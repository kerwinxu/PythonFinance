#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-10 19:59:17
# File Name: sample1.py
# import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])
# import pandas as pd
# from WindPy import w
# Import the backtrader platform
import backtrader as bt
import CerebroBase
import StrategyBase


# Create a Stratey
# 这个是自适应均线交易系统
class Strategy_KAMA(StrategyBase.StrategyBase):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # 添加自适应均线
        self.kama = bt.talib.KAMA(self.data)
        # To keep track of pending orders
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        k = self.kama
        h = self.data_high
        l = self.data_low
        p_s = self.position.size

        # 我的判断是，当最低价也高过均线价格。且单子少于等于0，就买入一部分，且设置止损价格为均线价格
        # 这里是连续2天突破均线才下单。
        if l[0] > k[0] and l[-1] > k[-1] and p_s <= 0:
            self.order = self.order_target_percent(target=0.1)
            self.sell(
                price=self.kama[0],
                size=self.order.size,
                executed=bt.Order.Stop,
                transmit=False,
                parent=self.order)
        if h[0] < k[0] and h[-1] < k[-1] and p_s >= 0:
            self.order = self.order_target_percent(target=-0.1)
            self.buy(
                price=self.kama[0],
                size=self.order.size,
                executed=bt.Order.Stop,
                transmit=False,
                parent=self.order)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_KAMA)

    # Set our desired cash start
    cerebro.set_cash(100000.0)

    cerebro.run()


times in msec
 clock   self+sourced   self:  sourced script
 clock   elapsed:              other lines

000.000  000.000: --- VIM STARTING ---
000.000  000.000: Allocated generic buffers
002.000  002.000: locale set
024.000  022.000: GUI prepared
024.000  000.000: clipboard setup
024.000  000.000: window checked
025.000  001.000: inits 1
035.000  010.000: parsing arguments
035.000  000.000: expanding arguments
036.000  001.000: shell init
036.000  000.000: inits 2
036.000  000.000: init highlight
042.000  002.000  002.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
042.000  003.000  001.000: sourcing D:\Vim\vim80\syntax\synload.vim
064.000  001.000  001.000: sourcing D:\Vim\vim80\lang/menu_chinese_gb.936.vim
064.000  001.000  000.000: sourcing D:\Vim\vim80\lang\menu_zh_cn.cp936.vim
065.000  000.000  000.000: sourcing D:\Vim\vim80\autoload\paste.vim
104.000  041.000  040.000: sourcing D:\Vim\vim80/menu.vim
104.000  061.000  020.000: sourcing D:\Vim\vim80\filetype.vim
104.000  066.000  002.000: sourcing D:\Vim\vim80\syntax\syntax.vim
105.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
105.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
107.000  001.000  001.000: sourcing D:\Vim\vim80\indent.vim
107.000  069.000  002.000: sourcing D:\Vim\vim80/defaults.vim
110.000  001.000  001.000: sourcing D:\Vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
110.000  073.000  003.000: sourcing D:\Vim\vim80/vimrc_example.vim
111.000  001.000  001.000: sourcing D:\Vim\vim80/mswin.vim
112.000  001.000  001.000: sourcing D:/gtags/share/gtags/gtags.vim
113.000  000.000  000.000: sourcing D:\Vim\vim80/delmenu.vim
115.000  001.000  001.000: sourcing D:\Vim\vim80\lang\menu_zh_cn.utf-8.vim
148.000  035.000  034.000: sourcing D:\Vim\vim80/menu.vim
150.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
150.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
151.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
152.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
152.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
153.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
154.000  001.000  001.000: sourcing D:\Vim\vim80\syntax/nosyntax.vim
155.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
155.000  001.000  001.000: sourcing D:\Vim\vim80\syntax\synload.vim
155.000  002.000  000.000: sourcing D:\Vim\vim80\syntax\syntax.vim
156.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
158.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
159.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
163.000  006.000  006.000: sourcing D:\Vim\vimfiles\colors\solarized.vim
167.000  002.000  002.000: sourcing D:\Vim\vim80\ftoff.vim
169.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\util.vim
170.000  003.000  002.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle.vim
170.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\init.vim
172.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\config.vim
173.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\autoload.vim
175.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\parser.vim
176.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\types\git.vim
215.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\ftdetect\xptemplate.detect.vim
216.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\ftdetect\xptlog.detect.vim
216.000  000.000  000.000: sourcing D:\Vim\bundle\.neobundle\ftdetect\ftdetect.vim
217.000  021.000  020.000: sourcing D:\Vim\vim80\filetype.vim
217.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
218.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
220.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\commands.vim
222.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\installer.vim
223.000  001.000  001.000: sourcing D:/Vim/bundle/NeoBundle.lock
225.000  188.000  039.000: sourcing $VIM\_vimrc
225.000  001.000: sourcing vimrc file(s)
226.000  000.000  000.000: sourcing D:\Vim\bundle\Gundo\plugin\gundo.vim
228.000  001.000  001.000: sourcing D:\Vim\bundle\Tagbar\plugin\tagbar.vim
229.000  001.000  001.000: sourcing D:\Vim\bundle\surround.vim\plugin\surround.vim
231.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\autoload\nerdtree.vim
233.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\path.vim
234.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\menu_controller.vim
235.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\menu_item.vim
235.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\key_map.vim
236.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\bookmark.vim
237.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\tree_file_node.vim
239.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\tree_dir_node.vim
240.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\opener.vim
241.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\creator.vim
242.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\flag_set.vim
243.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\nerdtree.vim
244.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\ui.vim
245.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\event.vim
245.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\notifier.vim
247.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\autoload\nerdtree\ui_glue.vim
264.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\nerdtree_plugin\exec_menuitem.vim
265.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\nerdtree_plugin\fs_menu.vim
266.000  036.000  032.000: sourcing D:\Vim\bundle\The-NERD-tree\plugin\NERD_tree.vim
268.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\autoload\XPT.vim
269.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
273.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\once.vim
275.000  004.000  003.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\cwd_snippet.vim
279.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\lib_filter.vim
279.000  004.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\lib_filter.vim
280.000  010.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
281.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
282.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\debug.vim
283.000  014.000  003.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
284.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
285.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpopup.vim
286.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
287.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
288.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpreplace.vim
290.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
291.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpreplace.vim
291.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
292.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpopup.vim
294.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\rctx.vim
297.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\flt.vim
299.000  010.000  007.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.vim
299.000  011.000  001.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpt.plugin.highlight.vim
300.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
301.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
301.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.parser.vim
301.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.vim
305.000  001.000  001.000: sourcing D:\Vim\bundle\AutoComplPop\autoload\acp.vim
306.000  004.000  003.000: sourcing D:\Vim\bundle\AutoComplPop\plugin\acp.vim
313.000  006.000  006.000: sourcing D:\Vim\bundle\YankRing.vim\plugin\yankring.vim
321.000  008.000  008.000: sourcing D:\Vim\bundle\The-NERD-Commenter\plugin\NERD_commenter.vim
324.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\getscriptPlugin.vim
325.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\gzip.vim
326.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\logiPat.vim
326.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\manpager.vim
327.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\matchparen.vim
328.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\netrwPlugin.vim
329.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\rrhelper.vim
329.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\spellfile.vim
330.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\tarPlugin.vim
331.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\tohtml.vim
332.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\vimballPlugin.vim
332.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\zipPlugin.vim
333.000  000.000  000.000: sourcing D:\Vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
334.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\plugin\neobundle.vim
334.000  019.000: loading plugins
334.000  000.000: loading packages
334.000  000.000: loading after plugins
334.000  000.000: inits 3
336.000  001.000  001.000: sourcing $VIMRUNTIME\menu.vim
522.000  187.000: starting GUI
524.000  002.000: reading viminfo
531.000  007.000: GUI delay
531.000  000.000: setting raw mode
531.000  000.000: start termcap
531.000  000.000: clearing screen
531.000  000.000: opening buffers
534.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\buf.vim
539.000  003.000  003.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\util.vim
543.000  008.000  005.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\msvr.vim
552.000  003.000  003.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\settingswitch.vim
553.000  009.000: BufEnter autocommands
553.000  000.000: editing files in windows
555.000  002.000: VimEnter autocommands
555.000  000.000: before starting main loop
561.000  006.000: first screen update
561.000  000.000: --- VIM STARTED ---


times in msec
 clock   self+sourced   self:  sourced script
 clock   elapsed:              other lines

000.000  000.000: --- VIM STARTING ---
000.000  000.000: Allocated generic buffers
002.000  002.000: locale set
026.000  024.000: GUI prepared
026.000  000.000: clipboard setup
026.000  000.000: window checked
027.000  001.000: inits 1
036.000  009.000: parsing arguments
036.000  000.000: expanding arguments
037.000  001.000: shell init
037.000  000.000: inits 2
037.000  000.000: init highlight
043.000  002.000  002.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
043.000  003.000  001.000: sourcing D:\Vim\vim80\syntax\synload.vim
068.000  001.000  001.000: sourcing D:\Vim\vim80\lang/menu_chinese_gb.936.vim
068.000  001.000  000.000: sourcing D:\Vim\vim80\lang\menu_zh_cn.cp936.vim
069.000  000.000  000.000: sourcing D:\Vim\vim80\autoload\paste.vim
111.000  045.000  044.000: sourcing D:\Vim\vim80/menu.vim
111.000  068.000  023.000: sourcing D:\Vim\vim80\filetype.vim
111.000  072.000  001.000: sourcing D:\Vim\vim80\syntax\syntax.vim
112.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
113.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
113.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
114.000  075.000  003.000: sourcing D:\Vim\vim80/defaults.vim
116.000  001.000  001.000: sourcing D:\Vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
116.000  078.000  002.000: sourcing D:\Vim\vim80/vimrc_example.vim
117.000  000.000  000.000: sourcing D:\Vim\vim80/mswin.vim
118.000  001.000  001.000: sourcing D:/gtags/share/gtags/gtags.vim
119.000  000.000  000.000: sourcing D:\Vim\vim80/delmenu.vim
120.000  000.000  000.000: sourcing D:\Vim\vim80\lang\menu_zh_cn.utf-8.vim
158.000  039.000  039.000: sourcing D:\Vim\vim80/menu.vim
160.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
160.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
160.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
161.000  000.000  000.000: sourcing D:\Vim\vim80\filetype.vim
161.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
162.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
163.000  000.000  000.000: sourcing D:\Vim\vim80\syntax/nosyntax.vim
164.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
164.000  001.000  001.000: sourcing D:\Vim\vim80\syntax\synload.vim
164.000  002.000  001.000: sourcing D:\Vim\vim80\syntax\syntax.vim
165.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
167.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
168.000  000.000  000.000: sourcing D:\Vim\vim80\syntax\syncolor.vim
171.000  005.000  005.000: sourcing D:\Vim\vimfiles\colors\solarized.vim
176.000  002.000  002.000: sourcing D:\Vim\vim80\ftoff.vim
178.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\util.vim
179.000  003.000  002.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle.vim
180.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\init.vim
181.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\config.vim
182.000  000.000  000.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\autoload.vim
184.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\parser.vim
186.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\types\git.vim
224.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\ftdetect\xptemplate.detect.vim
225.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\ftdetect\xptlog.detect.vim
225.000  000.000  000.000: sourcing D:\Vim\bundle\.neobundle\ftdetect\ftdetect.vim
226.000  021.000  021.000: sourcing D:\Vim\vim80\filetype.vim
226.000  000.000  000.000: sourcing D:\Vim\vim80\ftplugin.vim
227.000  000.000  000.000: sourcing D:\Vim\vim80\indent.vim
229.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\commands.vim
230.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\autoload\neobundle\installer.vim
232.000  001.000  001.000: sourcing D:/Vim/bundle/NeoBundle.lock
235.000  197.000  040.000: sourcing $VIM\_vimrc
235.000  001.000: sourcing vimrc file(s)
236.000  000.000  000.000: sourcing D:\Vim\bundle\Gundo\plugin\gundo.vim
237.000  000.000  000.000: sourcing D:\Vim\bundle\Tagbar\plugin\tagbar.vim
239.000  001.000  001.000: sourcing D:\Vim\bundle\surround.vim\plugin\surround.vim
241.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\autoload\nerdtree.vim
243.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\path.vim
244.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\menu_controller.vim
245.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\menu_item.vim
245.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\key_map.vim
246.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\bookmark.vim
248.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\tree_file_node.vim
249.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\tree_dir_node.vim
250.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\opener.vim
251.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\creator.vim
251.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\flag_set.vim
252.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\nerdtree.vim
253.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\ui.vim
254.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\event.vim
255.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\lib\nerdtree\notifier.vim
256.000  001.000  001.000: sourcing D:\Vim\bundle\The-NERD-tree\autoload\nerdtree\ui_glue.vim
274.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\nerdtree_plugin\exec_menuitem.vim
275.000  000.000  000.000: sourcing D:\Vim\bundle\The-NERD-tree\nerdtree_plugin\fs_menu.vim
276.000  037.000  029.000: sourcing D:\Vim\bundle\The-NERD-tree\plugin\NERD_tree.vim
279.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\XPT.vim
280.000  003.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
284.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\once.vim
286.000  004.000  003.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\cwd_snippet.vim
290.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\lib_filter.vim
290.000  004.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\option\lib_filter.vim
291.000  010.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
292.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
293.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\debug.vim
295.000  015.000  004.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
296.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
297.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpopup.vim
298.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\debug.vim
299.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
299.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpreplace.vim
301.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
301.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpreplace.vim
302.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpmark.vim
302.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpopup.vim
305.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\rctx.vim
307.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\flt.vim
309.000  009.000  004.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.vim
310.000  011.000  002.000: sourcing D:\Vim\bundle\xptemplate\plugin\xpt.plugin.highlight.vim
310.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
311.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.conf.vim
311.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.parser.vim
312.000  000.000  000.000: sourcing D:\Vim\bundle\xptemplate\plugin\xptemplate.vim
315.000  001.000  001.000: sourcing D:\Vim\bundle\AutoComplPop\autoload\acp.vim
315.000  002.000  001.000: sourcing D:\Vim\bundle\AutoComplPop\plugin\acp.vim
321.000  005.000  005.000: sourcing D:\Vim\bundle\YankRing.vim\plugin\yankring.vim
328.000  006.000  006.000: sourcing D:\Vim\bundle\The-NERD-Commenter\plugin\NERD_commenter.vim
330.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\getscriptPlugin.vim
331.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\gzip.vim
332.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\logiPat.vim
332.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\manpager.vim
333.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\matchparen.vim
334.000  001.000  001.000: sourcing D:\Vim\vim80\plugin\netrwPlugin.vim
334.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\rrhelper.vim
335.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\spellfile.vim
335.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\tarPlugin.vim
336.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\tohtml.vim
336.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\vimballPlugin.vim
337.000  000.000  000.000: sourcing D:\Vim\vim80\plugin\zipPlugin.vim
338.000  000.000  000.000: sourcing D:\Vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
339.000  001.000  001.000: sourcing D:\Vim\bundle\neobundle.vim\plugin\neobundle.vim
339.000  016.000: loading plugins
339.000  000.000: loading packages
339.000  000.000: loading after plugins
339.000  000.000: inits 3
341.000  002.000  002.000: sourcing $VIMRUNTIME\menu.vim
525.000  184.000: starting GUI
527.000  002.000: reading viminfo
535.000  008.000: GUI delay
535.000  000.000: setting raw mode
535.000  000.000: start termcap
536.000  001.000: clearing screen
537.000  001.000: opening buffers
539.000  001.000  001.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\buf.vim
545.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\util.vim
547.000  005.000  003.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\msvr.vim
554.000  002.000  002.000: sourcing D:\Vim\bundle\xptemplate\autoload\xpt\settingswitch.vim
554.000  009.000: BufEnter autocommands
554.000  000.000: editing files in windows
556.000  002.000: VimEnter autocommands
556.000  000.000: before starting main loop
560.000  004.000: first screen update
560.000  000.000: --- VIM STARTED ---
