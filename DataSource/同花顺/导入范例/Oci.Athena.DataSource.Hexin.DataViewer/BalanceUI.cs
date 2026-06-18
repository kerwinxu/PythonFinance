using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class BalanceUI : Form
{
	private IContainer components;

	private Splitter mSplitter;

	private DataGridView mComplexView;

	private BindingSource mBalanceBindingSource;

	private BindingSource mComplexBindingSource;

	private DataGridViewTextBoxColumn marketDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn symbolDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn freeNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn positionDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn recordNumberDataGridViewTextBoxColumn;

	private DataGridView mContentView;

	private DataGridViewTextBoxColumn dateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w1DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w2DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w3DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w4DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w5DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w6DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w7DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w8DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w9DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w10DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w11DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w12DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w13DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w14DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w15DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w16DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w17DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w18DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w19DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w20DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w21DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w22DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w23DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w24DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w25DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w26DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w27DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w28DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w29DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w30DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w31DataGridViewTextBoxColumn;

	private BalanceFile m_File;

	protected override void Dispose(bool disposing)
	{
		if (disposing && components != null)
		{
			components.Dispose();
		}
		base.Dispose(disposing);
	}

	private void InitializeComponent()
	{
		this.components = new System.ComponentModel.Container();
		System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle = new System.Windows.Forms.DataGridViewCellStyle();
		System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle2 = new System.Windows.Forms.DataGridViewCellStyle();
		System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle3 = new System.Windows.Forms.DataGridViewCellStyle();
		this.mContentView = new System.Windows.Forms.DataGridView();
		this.mBalanceBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.mSplitter = new System.Windows.Forms.Splitter();
		this.mComplexView = new System.Windows.Forms.DataGridView();
		this.marketDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.symbolDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.freeNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.positionDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.recordNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mComplexBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.dateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w1DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w2DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w3DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w4DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w5DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w6DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w7DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w8DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w9DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w10DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w11DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w12DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w13DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w14DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w15DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w16DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w17DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w18DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w19DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w20DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w21DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w22DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w23DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w24DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w25DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w26DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w27DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w28DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w29DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w30DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w31DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		((System.ComponentModel.ISupportInitialize)this.mContentView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mBalanceBindingSource).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).BeginInit();
		base.SuspendLayout();
		this.mContentView.AllowUserToAddRows = false;
		this.mContentView.AllowUserToDeleteRows = false;
		this.mContentView.AutoGenerateColumns = false;
		this.mContentView.BackgroundColor = System.Drawing.SystemColors.Window;
		this.mContentView.BorderStyle = System.Windows.Forms.BorderStyle.None;
		dataGridViewCellStyle.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		dataGridViewCellStyle.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
		this.mContentView.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle;
		this.mContentView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		this.mContentView.Columns.AddRange(this.dateDataGridViewTextBoxColumn, this.w1DataGridViewTextBoxColumn, this.w2DataGridViewTextBoxColumn, this.w3DataGridViewTextBoxColumn, this.w4DataGridViewTextBoxColumn, this.w5DataGridViewTextBoxColumn, this.w6DataGridViewTextBoxColumn, this.w7DataGridViewTextBoxColumn, this.w8DataGridViewTextBoxColumn, this.w9DataGridViewTextBoxColumn, this.w10DataGridViewTextBoxColumn, this.w11DataGridViewTextBoxColumn, this.w12DataGridViewTextBoxColumn, this.w13DataGridViewTextBoxColumn, this.w14DataGridViewTextBoxColumn, this.w15DataGridViewTextBoxColumn, this.w16DataGridViewTextBoxColumn, this.w17DataGridViewTextBoxColumn, this.w18DataGridViewTextBoxColumn, this.w19DataGridViewTextBoxColumn, this.w20DataGridViewTextBoxColumn, this.w21DataGridViewTextBoxColumn, this.w22DataGridViewTextBoxColumn, this.w23DataGridViewTextBoxColumn, this.w24DataGridViewTextBoxColumn, this.w25DataGridViewTextBoxColumn, this.w26DataGridViewTextBoxColumn, this.w27DataGridViewTextBoxColumn, this.w28DataGridViewTextBoxColumn, this.w29DataGridViewTextBoxColumn, this.w30DataGridViewTextBoxColumn, this.w31DataGridViewTextBoxColumn);
		this.mContentView.DataSource = this.mBalanceBindingSource;
		this.mContentView.Dock = System.Windows.Forms.DockStyle.Fill;
		this.mContentView.Location = new System.Drawing.Point(303, 0);
		this.mContentView.Name = "mContentView";
		this.mContentView.ReadOnly = true;
		this.mContentView.RowHeadersVisible = false;
		this.mContentView.RowTemplate.Height = 20;
		this.mContentView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mContentView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mContentView.Size = new System.Drawing.Size(289, 473);
		this.mContentView.TabIndex = 8;
		this.mBalanceBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.BalanceRecord);
		this.mSplitter.Location = new System.Drawing.Point(300, 0);
		this.mSplitter.Name = "mSplitter";
		this.mSplitter.Size = new System.Drawing.Size(3, 473);
		this.mSplitter.TabIndex = 7;
		this.mSplitter.TabStop = false;
		this.mComplexView.AllowUserToAddRows = false;
		this.mComplexView.AllowUserToDeleteRows = false;
		this.mComplexView.AutoGenerateColumns = false;
		this.mComplexView.BackgroundColor = System.Drawing.SystemColors.Window;
		this.mComplexView.BorderStyle = System.Windows.Forms.BorderStyle.None;
		dataGridViewCellStyle2.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle2.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle2.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle2.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle2.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle2.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		dataGridViewCellStyle2.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle2;
		this.mComplexView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		this.mComplexView.Columns.AddRange(this.marketDataGridViewTextBoxColumn, this.symbolDataGridViewTextBoxColumn, this.freeNumberDataGridViewTextBoxColumn, this.positionDataGridViewTextBoxColumn, this.recordNumberDataGridViewTextBoxColumn);
		this.mComplexView.DataSource = this.mComplexBindingSource;
		this.mComplexView.Dock = System.Windows.Forms.DockStyle.Left;
		this.mComplexView.Location = new System.Drawing.Point(0, 0);
		this.mComplexView.Name = "mComplexView";
		this.mComplexView.ReadOnly = true;
		dataGridViewCellStyle3.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle3.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle3.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle3.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle3.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle3.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		dataGridViewCellStyle3.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.RowHeadersDefaultCellStyle = dataGridViewCellStyle3;
		this.mComplexView.RowHeadersVisible = false;
		this.mComplexView.RowTemplate.Height = 20;
		this.mComplexView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mComplexView.Size = new System.Drawing.Size(300, 473);
		this.mComplexView.TabIndex = 6;
		this.marketDataGridViewTextBoxColumn.DataPropertyName = "Market";
		this.marketDataGridViewTextBoxColumn.HeaderText = "市场";
		this.marketDataGridViewTextBoxColumn.Name = "marketDataGridViewTextBoxColumn";
		this.marketDataGridViewTextBoxColumn.ReadOnly = true;
		this.symbolDataGridViewTextBoxColumn.DataPropertyName = "Symbol";
		this.symbolDataGridViewTextBoxColumn.HeaderText = "挂牌代码";
		this.symbolDataGridViewTextBoxColumn.Name = "symbolDataGridViewTextBoxColumn";
		this.symbolDataGridViewTextBoxColumn.ReadOnly = true;
		this.freeNumberDataGridViewTextBoxColumn.DataPropertyName = "FreeNumber";
		this.freeNumberDataGridViewTextBoxColumn.HeaderText = "空闲记录数";
		this.freeNumberDataGridViewTextBoxColumn.Name = "freeNumberDataGridViewTextBoxColumn";
		this.freeNumberDataGridViewTextBoxColumn.ReadOnly = true;
		this.positionDataGridViewTextBoxColumn.DataPropertyName = "Position";
		this.positionDataGridViewTextBoxColumn.HeaderText = "记录开始下标";
		this.positionDataGridViewTextBoxColumn.Name = "positionDataGridViewTextBoxColumn";
		this.positionDataGridViewTextBoxColumn.ReadOnly = true;
		this.recordNumberDataGridViewTextBoxColumn.DataPropertyName = "RecordNumber";
		this.recordNumberDataGridViewTextBoxColumn.HeaderText = "隶属记录数";
		this.recordNumberDataGridViewTextBoxColumn.Name = "recordNumberDataGridViewTextBoxColumn";
		this.recordNumberDataGridViewTextBoxColumn.ReadOnly = true;
		this.mComplexBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.ComplexIndexRecord);
		this.mComplexBindingSource.PositionChanged += new System.EventHandler(OnComplexPositionChangedEvent);
		this.dateDataGridViewTextBoxColumn.DataPropertyName = "Date";
		this.dateDataGridViewTextBoxColumn.HeaderText = "日期";
		this.dateDataGridViewTextBoxColumn.Name = "dateDataGridViewTextBoxColumn";
		this.dateDataGridViewTextBoxColumn.ReadOnly = true;
		this.w1DataGridViewTextBoxColumn.DataPropertyName = "W1";
		this.w1DataGridViewTextBoxColumn.HeaderText = "W1";
		this.w1DataGridViewTextBoxColumn.Name = "w1DataGridViewTextBoxColumn";
		this.w1DataGridViewTextBoxColumn.ReadOnly = true;
		this.w2DataGridViewTextBoxColumn.DataPropertyName = "W2";
		this.w2DataGridViewTextBoxColumn.HeaderText = "1 货币资金";
		this.w2DataGridViewTextBoxColumn.Name = "w2DataGridViewTextBoxColumn";
		this.w2DataGridViewTextBoxColumn.ReadOnly = true;
		this.w3DataGridViewTextBoxColumn.DataPropertyName = "W3";
		this.w3DataGridViewTextBoxColumn.HeaderText = "W3";
		this.w3DataGridViewTextBoxColumn.Name = "w3DataGridViewTextBoxColumn";
		this.w3DataGridViewTextBoxColumn.ReadOnly = true;
		this.w4DataGridViewTextBoxColumn.DataPropertyName = "W4";
		this.w4DataGridViewTextBoxColumn.HeaderText = "2 应收账款";
		this.w4DataGridViewTextBoxColumn.Name = "w4DataGridViewTextBoxColumn";
		this.w4DataGridViewTextBoxColumn.ReadOnly = true;
		this.w5DataGridViewTextBoxColumn.DataPropertyName = "W5";
		this.w5DataGridViewTextBoxColumn.HeaderText = "W5";
		this.w5DataGridViewTextBoxColumn.Name = "w5DataGridViewTextBoxColumn";
		this.w5DataGridViewTextBoxColumn.ReadOnly = true;
		this.w6DataGridViewTextBoxColumn.DataPropertyName = "W6";
		this.w6DataGridViewTextBoxColumn.HeaderText = "3 其他应收款";
		this.w6DataGridViewTextBoxColumn.Name = "w6DataGridViewTextBoxColumn";
		this.w6DataGridViewTextBoxColumn.ReadOnly = true;
		this.w7DataGridViewTextBoxColumn.DataPropertyName = "W7";
		this.w7DataGridViewTextBoxColumn.HeaderText = "4 预付款项";
		this.w7DataGridViewTextBoxColumn.Name = "w7DataGridViewTextBoxColumn";
		this.w7DataGridViewTextBoxColumn.ReadOnly = true;
		this.w8DataGridViewTextBoxColumn.DataPropertyName = "W8";
		this.w8DataGridViewTextBoxColumn.HeaderText = "W8";
		this.w8DataGridViewTextBoxColumn.Name = "w8DataGridViewTextBoxColumn";
		this.w8DataGridViewTextBoxColumn.ReadOnly = true;
		this.w9DataGridViewTextBoxColumn.DataPropertyName = "W9";
		this.w9DataGridViewTextBoxColumn.HeaderText = "5 存货";
		this.w9DataGridViewTextBoxColumn.Name = "w9DataGridViewTextBoxColumn";
		this.w9DataGridViewTextBoxColumn.ReadOnly = true;
		this.w10DataGridViewTextBoxColumn.DataPropertyName = "W10";
		this.w10DataGridViewTextBoxColumn.HeaderText = "W10";
		this.w10DataGridViewTextBoxColumn.Name = "w10DataGridViewTextBoxColumn";
		this.w10DataGridViewTextBoxColumn.ReadOnly = true;
		this.w11DataGridViewTextBoxColumn.DataPropertyName = "W11";
		this.w11DataGridViewTextBoxColumn.HeaderText = "W11";
		this.w11DataGridViewTextBoxColumn.Name = "w11DataGridViewTextBoxColumn";
		this.w11DataGridViewTextBoxColumn.ReadOnly = true;
		this.w12DataGridViewTextBoxColumn.DataPropertyName = "W12";
		this.w12DataGridViewTextBoxColumn.HeaderText = "6 流动资产合计";
		this.w12DataGridViewTextBoxColumn.Name = "w12DataGridViewTextBoxColumn";
		this.w12DataGridViewTextBoxColumn.ReadOnly = true;
		this.w13DataGridViewTextBoxColumn.DataPropertyName = "W13";
		this.w13DataGridViewTextBoxColumn.HeaderText = "W13";
		this.w13DataGridViewTextBoxColumn.Name = "w13DataGridViewTextBoxColumn";
		this.w13DataGridViewTextBoxColumn.ReadOnly = true;
		this.w14DataGridViewTextBoxColumn.DataPropertyName = "W14";
		this.w14DataGridViewTextBoxColumn.HeaderText = "W14";
		this.w14DataGridViewTextBoxColumn.Name = "w14DataGridViewTextBoxColumn";
		this.w14DataGridViewTextBoxColumn.ReadOnly = true;
		this.w15DataGridViewTextBoxColumn.DataPropertyName = "W15";
		this.w15DataGridViewTextBoxColumn.HeaderText = "7 固定资产原值";
		this.w15DataGridViewTextBoxColumn.Name = "w15DataGridViewTextBoxColumn";
		this.w15DataGridViewTextBoxColumn.ReadOnly = true;
		this.w16DataGridViewTextBoxColumn.DataPropertyName = "W16";
		this.w16DataGridViewTextBoxColumn.HeaderText = "W16";
		this.w16DataGridViewTextBoxColumn.Name = "w16DataGridViewTextBoxColumn";
		this.w16DataGridViewTextBoxColumn.ReadOnly = true;
		this.w17DataGridViewTextBoxColumn.DataPropertyName = "W17";
		this.w17DataGridViewTextBoxColumn.HeaderText = "W17";
		this.w17DataGridViewTextBoxColumn.Name = "w17DataGridViewTextBoxColumn";
		this.w17DataGridViewTextBoxColumn.ReadOnly = true;
		this.w18DataGridViewTextBoxColumn.DataPropertyName = "W18";
		this.w18DataGridViewTextBoxColumn.HeaderText = "8 无形资产净额";
		this.w18DataGridViewTextBoxColumn.Name = "w18DataGridViewTextBoxColumn";
		this.w18DataGridViewTextBoxColumn.ReadOnly = true;
		this.w19DataGridViewTextBoxColumn.DataPropertyName = "W19";
		this.w19DataGridViewTextBoxColumn.HeaderText = "W19";
		this.w19DataGridViewTextBoxColumn.Name = "w19DataGridViewTextBoxColumn";
		this.w19DataGridViewTextBoxColumn.ReadOnly = true;
		this.w20DataGridViewTextBoxColumn.DataPropertyName = "W20";
		this.w20DataGridViewTextBoxColumn.HeaderText = "W20";
		this.w20DataGridViewTextBoxColumn.Name = "w20DataGridViewTextBoxColumn";
		this.w20DataGridViewTextBoxColumn.ReadOnly = true;
		this.w21DataGridViewTextBoxColumn.DataPropertyName = "W21";
		this.w21DataGridViewTextBoxColumn.HeaderText = "9 资产总计";
		this.w21DataGridViewTextBoxColumn.Name = "w21DataGridViewTextBoxColumn";
		this.w21DataGridViewTextBoxColumn.ReadOnly = true;
		this.w22DataGridViewTextBoxColumn.DataPropertyName = "W22";
		this.w22DataGridViewTextBoxColumn.HeaderText = "10 短期借款";
		this.w22DataGridViewTextBoxColumn.Name = "w22DataGridViewTextBoxColumn";
		this.w22DataGridViewTextBoxColumn.ReadOnly = true;
		this.w23DataGridViewTextBoxColumn.DataPropertyName = "W23";
		this.w23DataGridViewTextBoxColumn.HeaderText = "11 应付账款";
		this.w23DataGridViewTextBoxColumn.Name = "w23DataGridViewTextBoxColumn";
		this.w23DataGridViewTextBoxColumn.ReadOnly = true;
		this.w24DataGridViewTextBoxColumn.DataPropertyName = "W24";
		this.w24DataGridViewTextBoxColumn.HeaderText = "12 流动负债合计";
		this.w24DataGridViewTextBoxColumn.Name = "w24DataGridViewTextBoxColumn";
		this.w24DataGridViewTextBoxColumn.ReadOnly = true;
		this.w25DataGridViewTextBoxColumn.DataPropertyName = "W25";
		this.w25DataGridViewTextBoxColumn.HeaderText = "13 长期借款";
		this.w25DataGridViewTextBoxColumn.Name = "w25DataGridViewTextBoxColumn";
		this.w25DataGridViewTextBoxColumn.ReadOnly = true;
		this.w26DataGridViewTextBoxColumn.DataPropertyName = "W26";
		this.w26DataGridViewTextBoxColumn.HeaderText = "W26";
		this.w26DataGridViewTextBoxColumn.Name = "w26DataGridViewTextBoxColumn";
		this.w26DataGridViewTextBoxColumn.ReadOnly = true;
		this.w27DataGridViewTextBoxColumn.DataPropertyName = "W27";
		this.w27DataGridViewTextBoxColumn.HeaderText = "14 负债合计";
		this.w27DataGridViewTextBoxColumn.Name = "w27DataGridViewTextBoxColumn";
		this.w27DataGridViewTextBoxColumn.ReadOnly = true;
		this.w28DataGridViewTextBoxColumn.DataPropertyName = "W28";
		this.w28DataGridViewTextBoxColumn.HeaderText = "15 资本公积";
		this.w28DataGridViewTextBoxColumn.Name = "w28DataGridViewTextBoxColumn";
		this.w28DataGridViewTextBoxColumn.ReadOnly = true;
		this.w29DataGridViewTextBoxColumn.DataPropertyName = "W29";
		this.w29DataGridViewTextBoxColumn.HeaderText = "16 盈余公积";
		this.w29DataGridViewTextBoxColumn.Name = "w29DataGridViewTextBoxColumn";
		this.w29DataGridViewTextBoxColumn.ReadOnly = true;
		this.w30DataGridViewTextBoxColumn.DataPropertyName = "W30";
		this.w30DataGridViewTextBoxColumn.HeaderText = "17 所有者权益（或股东权益）合计";
		this.w30DataGridViewTextBoxColumn.Name = "w30DataGridViewTextBoxColumn";
		this.w30DataGridViewTextBoxColumn.ReadOnly = true;
		this.w31DataGridViewTextBoxColumn.DataPropertyName = "W31";
		this.w31DataGridViewTextBoxColumn.HeaderText = "18 负债和所有者（或股东权益）合计";
		this.w31DataGridViewTextBoxColumn.Name = "w31DataGridViewTextBoxColumn";
		this.w31DataGridViewTextBoxColumn.ReadOnly = true;
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 473);
		base.Controls.Add(this.mContentView);
		base.Controls.Add(this.mSplitter);
		base.Controls.Add(this.mComplexView);
		base.Name = "BalanceUI";
		this.Text = "资产负债";
		((System.ComponentModel.ISupportInitialize)this.mContentView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mBalanceBindingSource).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).EndInit();
		base.ResumeLayout(false);
	}

	public BalanceUI()
	{
		InitializeComponent();
	}

	public void Initialize(string filename)
	{
		if (!File.Exists(filename))
		{
			return;
		}
		Text = Path.GetFileNameWithoutExtension(filename) + " - " + Text;
		bool flag = false;
		using (FileStream stream = File.OpenRead(filename))
		{
			m_File = default(BalanceFile);
			flag = BalanceFile.Read(ref m_File, stream);
		}
		if (!flag)
		{
			return;
		}
		mComplexBindingSource.SuspendBinding();
		try
		{
			List<ComplexIndexRecord> list = new List<ComplexIndexRecord>(m_File.Block.RecordList);
			list.Sort((ComplexIndexRecord x, ComplexIndexRecord y) => x.Symbol.CompareTo(y.Symbol));
			mComplexBindingSource.Clear();
			foreach (ComplexIndexRecord item in list)
			{
				mComplexBindingSource.Add(item);
			}
			mComplexBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mComplexBindingSource.ResumeBinding();
		}
	}

	private void OnComplexPositionChangedEvent(object sender, EventArgs e)
	{
		mBalanceBindingSource.SuspendBinding();
		try
		{
			mBalanceBindingSource.Clear();
			ComplexIndexRecord complexIndexRecord = (ComplexIndexRecord)mComplexBindingSource[mComplexBindingSource.Position];
			for (int i = 0; i < complexIndexRecord.RecordNumber; i++)
			{
				if (m_File.RecordList[i + complexIndexRecord.Position].Date > DateTime.MinValue)
				{
					mBalanceBindingSource.Add(m_File.RecordList[i + complexIndexRecord.Position]);
				}
			}
			mBalanceBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mBalanceBindingSource.ResumeBinding();
		}
	}
}
