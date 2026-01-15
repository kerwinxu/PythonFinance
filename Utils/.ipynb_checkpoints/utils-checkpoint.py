import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import talib
import torch.utils.data as Data
# 这里要试试绘图
# 这里要试试绘图
from visdom import Visdom
from PIL import Image
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.optim.lr_scheduler import StepLR

is_print_line = False

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if is_print_line:
    vis = Visdom()

def do_train(epoch_count, loader, net, optimizer, loss_fun, train_line_name='train_line'):
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)
    # scheduler = StepLR(optimizer, step_size=10, gamma=0.1)
    if is_print_line:
        vis.line([0.], [0], win=train_line_name, opts=dict(title=train_line_name))
        _step = 1
    for epoch in range(epoch_count):  # 迭代
        arr_loss = []  # 记录损失
        arr_labels = []  # 实际值的平均
        for i, data in enumerate(loader, 0):
            # 获取输入
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            # 正向传播，反向传播，优化
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = loss_fun(outputs, labels)
            loss.backward()
            optimizer.step()
            
            # 这里更新到显示
            if epoch > 0:
                if is_print_line:
                    vis.line([loss.cpu().detach().numpy()], [_step], win=train_line_name, update='append')
                    _step = _step + 1
            arr_loss.append(loss.item())
            labels2 = torch.abs(labels)
            arr_labels.append((sum(labels2)/len(labels2)).item())
        scheduler.step(loss)  # 根据损失函数优化学习率
        # scheduler.step()
        if len(arr_loss) > 0 and len(arr_labels) > 0:
            loss_arg = sum(arr_loss)/len(arr_loss)
            labels_arg = sum(arr_labels)/len(arr_labels)
            print(f'{epoch+1}, avg labels: {labels_arg:.5f} avg loss:{loss_arg:.5f}, max loss: {max(arr_loss):.5f}, min loss : {min(arr_loss):.5f}')


def do_test(loader,net ,loss_fun, test_line_name='test_line'):
    if is_print_line:
        _step = 1
        vis.line([0.], [0], win=test_line_name, opts=dict(title=test_line_name))
    arr_loss = []
    with torch.no_grad():
        for i, data in enumerate(loader, 0):
                # 获取输入
                inputs, labels = data
                inputs = inputs.to(device)
                labels = labels.to(device)
                # 正向传播，反向传播，优化
                outputs = net(inputs)
                loss = loss_fun(outputs, labels)
                arr_loss.append(loss.item())
                # 这里更新到显示
                if is_print_line:
                    vis.line([loss.cpu().detach().numpy()], [_step], win=test_line_name, update='append')
                    _step = _step + 1
    print(f'实际值:', labels) 
    print(f'预测值:', outputs)
    print(f'test : max loss : {max(arr_loss)}, min loss: {min(arr_loss)}, avg loss : {sum(arr_loss)/len(arr_loss)}')