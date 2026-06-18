using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class CashflowUI : Form
{
	private CashflowFile m_File;

	private IContainer components;

	private DataGridView mContentView;

	private Splitter mSplitter;

	private DataGridView mComplexView;

	private BindingSource mCashflowBindingSource;

	private BindingSource mComplexBindingSource;

	private DataGridViewTextBoxColumn marketDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn symbolDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn freeNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn positionDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn recordNumberDataGridViewTextBoxColumn;

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

	private DataGridViewTextBoxColumn w32DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w33DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w34DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w35DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w36DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w37DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w38DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w39DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w40DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w41DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w42DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w43DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w44DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w45DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w46DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w47DataGridViewTextBoxColumn;

	public CashflowUI()
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
			m_File = default(CashflowFile);
			flag = CashflowFile.Read(ref m_File, stream);
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
		for (int num = 0; num < mContentView.Columns.Count; num++)
		{
			if (mContentView.Columns[num].CellType.Equals(typeof(double)))
			{
				mContentView.Columns[num].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleRight;
				mContentView.Columns[num].DefaultCellStyle.Format = "N3";
			}
		}
	}

	private void OnComplexPositionChangedEvent(object sender, EventArgs e)
	{
		mCashflowBindingSource.SuspendBinding();
		try
		{
			mCashflowBindingSource.Clear();
			ComplexIndexRecord complexIndexRecord = (ComplexIndexRecord)mComplexBindingSource[mComplexBindingSource.Position];
			for (int i = 0; i < complexIndexRecord.RecordNumber; i++)
			{
				if (m_File.RecordList[i + complexIndexRecord.Position].Date > DateTime.MinValue)
				{
					mCashflowBindingSource.Add(m_File.RecordList[i + complexIndexRecord.Position]);
				}
			}
			mCashflowBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mCashflowBindingSource.ResumeBinding();
		}
	}

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
		this.mContentView = new System.Windows.Forms.DataGridView();
		this.mSplitter = new System.Windows.Forms.Splitter();
		this.mComplexView = new System.Windows.Forms.DataGridView();
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
		this.w32DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w33DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w34DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w35DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w36DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w37DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w38DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w39DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w40DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w41DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w42DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w43DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w44DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w45DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w46DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w47DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mCashflowBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.marketDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.symbolDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.freeNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.positionDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.recordNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mComplexBindingSource = new System.Windows.Forms.BindingSource(this.components);
		((System.ComponentModel.ISupportInitialize)this.mContentView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mCashflowBindingSource).BeginInit();
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
		this.mContentView.Columns.AddRange(this.dateDataGridViewTextBoxColumn, this.w1DataGridViewTextBoxColumn, this.w2DataGridViewTextBoxColumn, this.w3DataGridViewTextBoxColumn, this.w4DataGridViewTextBoxColumn, this.w5DataGridViewTextBoxColumn, this.w6DataGridViewTextBoxColumn, this.w7DataGridViewTextBoxColumn, this.w8DataGridViewTextBoxColumn, this.w9DataGridViewTextBoxColumn, this.w10DataGridViewTextBoxColumn, this.w11DataGridViewTextBoxColumn, this.w12DataGridViewTextBoxColumn, this.w13DataGridViewTextBoxColumn, this.w14DataGridViewTextBoxColumn, this.w15DataGridViewTextBoxColumn, this.w16DataGridViewTextBoxColumn, this.w17DataGridViewTextBoxColumn, this.w18DataGridViewTextBoxColumn, this.w19DataGridViewTextBoxColumn, this.w20DataGridViewTextBoxColumn, this.w21DataGridViewTextBoxColumn, this.w22DataGridViewTextBoxColumn, this.w23DataGridViewTextBoxColumn, this.w24DataGridViewTextBoxColumn, this.w25DataGridViewTextBoxColumn, this.w26DataGridViewTextBoxColumn, this.w27DataGridViewTextBoxColumn, this.w28DataGridViewTextBoxColumn, this.w29DataGridViewTextBoxColumn, this.w30DataGridViewTextBoxColumn, this.w31DataGridViewTextBoxColumn, this.w32DataGridViewTextBoxColumn, this.w33DataGridViewTextBoxColumn, this.w34DataGridViewTextBoxColumn, this.w35DataGridViewTextBoxColumn, this.w36DataGridViewTextBoxColumn, this.w37DataGridViewTextBoxColumn, this.w38DataGridViewTextBoxColumn, this.w39DataGridViewTextBoxColumn, this.w40DataGridViewTextBoxColumn, this.w41DataGridViewTextBoxColumn, this.w42DataGridViewTextBoxColumn, this.w43DataGridViewTextBoxColumn, this.w44DataGridViewTextBoxColumn, this.w45DataGridViewTextBoxColumn, this.w46DataGridViewTextBoxColumn, this.w47DataGridViewTextBoxColumn);
		this.mContentView.DataSource = this.mCashflowBindingSource;
		this.mContentView.Dock = System.Windows.Forms.DockStyle.Fill;
		this.mContentView.Location = new System.Drawing.Point(303, 0);
		this.mContentView.Name = "mContentView";
		this.mContentView.ReadOnly = true;
		this.mContentView.RowHeadersVisible = false;
		this.mContentView.RowTemplate.Height = 20;
		this.mContentView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mContentView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mContentView.Size = new System.Drawing.Size(289, 473);
		this.mContentView.TabIndex = 5;
		this.mSplitter.Location = new System.Drawing.Point(300, 0);
		this.mSplitter.Name = "mSplitter";
		this.mSplitter.Size = new System.Drawing.Size(3, 473);
		this.mSplitter.TabIndex = 4;
		this.mSplitter.TabStop = false;
		this.mComplexView.AllowUserToAddRows = false;
		this.mComplexView.AllowUserToDeleteRows = false;
		this.mComplexView.AutoGenerateColumns = false;
		this.mComplexView.BackgroundColor = System.Drawing.SystemColors.Window;
		this.mComplexView.BorderStyle = System.Windows.Forms.BorderStyle.None;
		this.mComplexView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		this.mComplexView.Columns.AddRange(this.marketDataGridViewTextBoxColumn, this.symbolDataGridViewTextBoxColumn, this.freeNumberDataGridViewTextBoxColumn, this.positionDataGridViewTextBoxColumn, this.recordNumberDataGridViewTextBoxColumn);
		this.mComplexView.DataSource = this.mComplexBindingSource;
		this.mComplexView.Dock = System.Windows.Forms.DockStyle.Left;
		this.mComplexView.Location = new System.Drawing.Point(0, 0);
		this.mComplexView.Name = "mComplexView";
		this.mComplexView.ReadOnly = true;
		dataGridViewCellStyle2.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle2.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle2.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle2.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle2.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle2.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		dataGridViewCellStyle2.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.RowHeadersDefaultCellStyle = dataGridViewCellStyle2;
		this.mComplexView.RowHeadersVisible = false;
		this.mComplexView.RowTemplate.Height = 20;
		this.mComplexView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mComplexView.Size = new System.Drawing.Size(300, 473);
		this.mComplexView.TabIndex = 3;
		this.dateDataGridViewTextBoxColumn.DataPropertyName = "Date";
		this.dateDataGridViewTextBoxColumn.HeaderText = "日期";
		this.dateDataGridViewTextBoxColumn.Name = "dateDataGridViewTextBoxColumn";
		this.dateDataGridViewTextBoxColumn.ReadOnly = true;
		this.w1DataGridViewTextBoxColumn.DataPropertyName = "W1";
		this.w1DataGridViewTextBoxColumn.HeaderText = "W1";
		this.w1DataGridViewTextBoxColumn.Name = "w1DataGridViewTextBoxColumn";
		this.w1DataGridViewTextBoxColumn.ReadOnly = true;
		this.w2DataGridViewTextBoxColumn.DataPropertyName = "W2";
		this.w2DataGridViewTextBoxColumn.HeaderText = "1 销售商品、提供劳务收到的现金";
		this.w2DataGridViewTextBoxColumn.Name = "w2DataGridViewTextBoxColumn";
		this.w2DataGridViewTextBoxColumn.ReadOnly = true;
		this.w3DataGridViewTextBoxColumn.DataPropertyName = "W3";
		this.w3DataGridViewTextBoxColumn.HeaderText = "W3";
		this.w3DataGridViewTextBoxColumn.Name = "w3DataGridViewTextBoxColumn";
		this.w3DataGridViewTextBoxColumn.ReadOnly = true;
		this.w4DataGridViewTextBoxColumn.DataPropertyName = "W4";
		this.w4DataGridViewTextBoxColumn.HeaderText = "2 收到的税费返还";
		this.w4DataGridViewTextBoxColumn.Name = "w4DataGridViewTextBoxColumn";
		this.w4DataGridViewTextBoxColumn.ReadOnly = true;
		this.w5DataGridViewTextBoxColumn.DataPropertyName = "W5";
		this.w5DataGridViewTextBoxColumn.HeaderText = "3 收到其他与经营活动有关的现金";
		this.w5DataGridViewTextBoxColumn.Name = "w5DataGridViewTextBoxColumn";
		this.w5DataGridViewTextBoxColumn.ReadOnly = true;
		this.w6DataGridViewTextBoxColumn.DataPropertyName = "W6";
		this.w6DataGridViewTextBoxColumn.HeaderText = "4 经营活动现金流入小计";
		this.w6DataGridViewTextBoxColumn.Name = "w6DataGridViewTextBoxColumn";
		this.w6DataGridViewTextBoxColumn.ReadOnly = true;
		this.w7DataGridViewTextBoxColumn.DataPropertyName = "W7";
		this.w7DataGridViewTextBoxColumn.HeaderText = "5 购买商品、接受劳务支付的现金";
		this.w7DataGridViewTextBoxColumn.Name = "w7DataGridViewTextBoxColumn";
		this.w7DataGridViewTextBoxColumn.ReadOnly = true;
		this.w8DataGridViewTextBoxColumn.DataPropertyName = "W8";
		this.w8DataGridViewTextBoxColumn.HeaderText = "W8";
		this.w8DataGridViewTextBoxColumn.Name = "w8DataGridViewTextBoxColumn";
		this.w8DataGridViewTextBoxColumn.ReadOnly = true;
		this.w9DataGridViewTextBoxColumn.DataPropertyName = "W9";
		this.w9DataGridViewTextBoxColumn.HeaderText = "6 支付给职工以及为职工支付的现金";
		this.w9DataGridViewTextBoxColumn.Name = "w9DataGridViewTextBoxColumn";
		this.w9DataGridViewTextBoxColumn.ReadOnly = true;
		this.w10DataGridViewTextBoxColumn.DataPropertyName = "W10";
		this.w10DataGridViewTextBoxColumn.HeaderText = "7 支付的各项税费";
		this.w10DataGridViewTextBoxColumn.Name = "w10DataGridViewTextBoxColumn";
		this.w10DataGridViewTextBoxColumn.ReadOnly = true;
		this.w11DataGridViewTextBoxColumn.DataPropertyName = "W11";
		this.w11DataGridViewTextBoxColumn.HeaderText = "W11";
		this.w11DataGridViewTextBoxColumn.Name = "w11DataGridViewTextBoxColumn";
		this.w11DataGridViewTextBoxColumn.ReadOnly = true;
		this.w12DataGridViewTextBoxColumn.DataPropertyName = "W12";
		this.w12DataGridViewTextBoxColumn.HeaderText = "W12";
		this.w12DataGridViewTextBoxColumn.Name = "w12DataGridViewTextBoxColumn";
		this.w12DataGridViewTextBoxColumn.ReadOnly = true;
		this.w13DataGridViewTextBoxColumn.DataPropertyName = "W13";
		this.w13DataGridViewTextBoxColumn.HeaderText = "8 支付的其它与经营活动有关的现金";
		this.w13DataGridViewTextBoxColumn.Name = "w13DataGridViewTextBoxColumn";
		this.w13DataGridViewTextBoxColumn.ReadOnly = true;
		this.w14DataGridViewTextBoxColumn.DataPropertyName = "W14";
		this.w14DataGridViewTextBoxColumn.HeaderText = "9 经营活动现金流出小计";
		this.w14DataGridViewTextBoxColumn.Name = "w14DataGridViewTextBoxColumn";
		this.w14DataGridViewTextBoxColumn.ReadOnly = true;
		this.w15DataGridViewTextBoxColumn.DataPropertyName = "W15";
		this.w15DataGridViewTextBoxColumn.HeaderText = "10 经营活动产生的现金流量净额";
		this.w15DataGridViewTextBoxColumn.Name = "w15DataGridViewTextBoxColumn";
		this.w15DataGridViewTextBoxColumn.ReadOnly = true;
		this.w16DataGridViewTextBoxColumn.DataPropertyName = "W16";
		this.w16DataGridViewTextBoxColumn.HeaderText = "11 收回投资收到的现金";
		this.w16DataGridViewTextBoxColumn.Name = "w16DataGridViewTextBoxColumn";
		this.w16DataGridViewTextBoxColumn.ReadOnly = true;
		this.w17DataGridViewTextBoxColumn.DataPropertyName = "W17";
		this.w17DataGridViewTextBoxColumn.HeaderText = "12 取得投资收益所收到的现金";
		this.w17DataGridViewTextBoxColumn.Name = "w17DataGridViewTextBoxColumn";
		this.w17DataGridViewTextBoxColumn.ReadOnly = true;
		this.w18DataGridViewTextBoxColumn.DataPropertyName = "W18";
		this.w18DataGridViewTextBoxColumn.HeaderText = "W18";
		this.w18DataGridViewTextBoxColumn.Name = "w18DataGridViewTextBoxColumn";
		this.w18DataGridViewTextBoxColumn.ReadOnly = true;
		this.w19DataGridViewTextBoxColumn.DataPropertyName = "W19";
		this.w19DataGridViewTextBoxColumn.HeaderText = "13 处置固定资产、无形资产和其它长期资产而收回的现金净额";
		this.w19DataGridViewTextBoxColumn.Name = "w19DataGridViewTextBoxColumn";
		this.w19DataGridViewTextBoxColumn.ReadOnly = true;
		this.w20DataGridViewTextBoxColumn.DataPropertyName = "W20";
		this.w20DataGridViewTextBoxColumn.HeaderText = "14 收到的其他与投资活动有关的现金";
		this.w20DataGridViewTextBoxColumn.Name = "w20DataGridViewTextBoxColumn";
		this.w20DataGridViewTextBoxColumn.ReadOnly = true;
		this.w21DataGridViewTextBoxColumn.DataPropertyName = "W21";
		this.w21DataGridViewTextBoxColumn.HeaderText = "15 投资活动现金流入小计";
		this.w21DataGridViewTextBoxColumn.Name = "w21DataGridViewTextBoxColumn";
		this.w21DataGridViewTextBoxColumn.ReadOnly = true;
		this.w22DataGridViewTextBoxColumn.DataPropertyName = "W22";
		this.w22DataGridViewTextBoxColumn.HeaderText = "16 购建固定资产、无形资产和其它长期资产所支付的现金";
		this.w22DataGridViewTextBoxColumn.Name = "w22DataGridViewTextBoxColumn";
		this.w22DataGridViewTextBoxColumn.ReadOnly = true;
		this.w23DataGridViewTextBoxColumn.DataPropertyName = "W23";
		this.w23DataGridViewTextBoxColumn.HeaderText = "17 投资支付的现金";
		this.w23DataGridViewTextBoxColumn.Name = "w23DataGridViewTextBoxColumn";
		this.w23DataGridViewTextBoxColumn.ReadOnly = true;
		this.w24DataGridViewTextBoxColumn.DataPropertyName = "W24";
		this.w24DataGridViewTextBoxColumn.HeaderText = "W24";
		this.w24DataGridViewTextBoxColumn.Name = "w24DataGridViewTextBoxColumn";
		this.w24DataGridViewTextBoxColumn.ReadOnly = true;
		this.w25DataGridViewTextBoxColumn.DataPropertyName = "W25";
		this.w25DataGridViewTextBoxColumn.HeaderText = "18 支付的其他与投资活动有关的现金";
		this.w25DataGridViewTextBoxColumn.Name = "w25DataGridViewTextBoxColumn";
		this.w25DataGridViewTextBoxColumn.ReadOnly = true;
		this.w26DataGridViewTextBoxColumn.DataPropertyName = "W26";
		this.w26DataGridViewTextBoxColumn.HeaderText = "19 投资活动现金流出小计";
		this.w26DataGridViewTextBoxColumn.Name = "w26DataGridViewTextBoxColumn";
		this.w26DataGridViewTextBoxColumn.ReadOnly = true;
		this.w27DataGridViewTextBoxColumn.DataPropertyName = "W27";
		this.w27DataGridViewTextBoxColumn.HeaderText = "20 投资活动产生的现金流量净额";
		this.w27DataGridViewTextBoxColumn.Name = "w27DataGridViewTextBoxColumn";
		this.w27DataGridViewTextBoxColumn.ReadOnly = true;
		this.w28DataGridViewTextBoxColumn.DataPropertyName = "W28";
		this.w28DataGridViewTextBoxColumn.HeaderText = "21 吸收投资所收到的现金";
		this.w28DataGridViewTextBoxColumn.Name = "w28DataGridViewTextBoxColumn";
		this.w28DataGridViewTextBoxColumn.ReadOnly = true;
		this.w29DataGridViewTextBoxColumn.DataPropertyName = "W29";
		this.w29DataGridViewTextBoxColumn.HeaderText = "22 发行债券收到的现金";
		this.w29DataGridViewTextBoxColumn.Name = "w29DataGridViewTextBoxColumn";
		this.w29DataGridViewTextBoxColumn.ReadOnly = true;
		this.w30DataGridViewTextBoxColumn.DataPropertyName = "W30";
		this.w30DataGridViewTextBoxColumn.HeaderText = "23 借款所收到的现金";
		this.w30DataGridViewTextBoxColumn.Name = "w30DataGridViewTextBoxColumn";
		this.w30DataGridViewTextBoxColumn.ReadOnly = true;
		this.w31DataGridViewTextBoxColumn.DataPropertyName = "W31";
		this.w31DataGridViewTextBoxColumn.HeaderText = "24 收到的其他与筹资活动有关的现金";
		this.w31DataGridViewTextBoxColumn.Name = "w31DataGridViewTextBoxColumn";
		this.w31DataGridViewTextBoxColumn.ReadOnly = true;
		this.w32DataGridViewTextBoxColumn.DataPropertyName = "W32";
		this.w32DataGridViewTextBoxColumn.HeaderText = "25 筹资活动现金流入小计";
		this.w32DataGridViewTextBoxColumn.Name = "w32DataGridViewTextBoxColumn";
		this.w32DataGridViewTextBoxColumn.ReadOnly = true;
		this.w33DataGridViewTextBoxColumn.DataPropertyName = "W33";
		this.w33DataGridViewTextBoxColumn.HeaderText = "26 偿还债务所支付的现金";
		this.w33DataGridViewTextBoxColumn.Name = "w33DataGridViewTextBoxColumn";
		this.w33DataGridViewTextBoxColumn.ReadOnly = true;
		this.w34DataGridViewTextBoxColumn.DataPropertyName = "W34";
		this.w34DataGridViewTextBoxColumn.HeaderText = "W34";
		this.w34DataGridViewTextBoxColumn.Name = "w34DataGridViewTextBoxColumn";
		this.w34DataGridViewTextBoxColumn.ReadOnly = true;
		this.w35DataGridViewTextBoxColumn.DataPropertyName = "W35";
		this.w35DataGridViewTextBoxColumn.HeaderText = "27 分配股利或利润所支付的现金";
		this.w35DataGridViewTextBoxColumn.Name = "w35DataGridViewTextBoxColumn";
		this.w35DataGridViewTextBoxColumn.ReadOnly = true;
		this.w36DataGridViewTextBoxColumn.DataPropertyName = "W36";
		this.w36DataGridViewTextBoxColumn.HeaderText = "28 其中：子公司支付少数股东的股利";
		this.w36DataGridViewTextBoxColumn.Name = "w36DataGridViewTextBoxColumn";
		this.w36DataGridViewTextBoxColumn.ReadOnly = true;
		this.w37DataGridViewTextBoxColumn.DataPropertyName = "W37";
		this.w37DataGridViewTextBoxColumn.HeaderText = "W37";
		this.w37DataGridViewTextBoxColumn.Name = "w37DataGridViewTextBoxColumn";
		this.w37DataGridViewTextBoxColumn.ReadOnly = true;
		this.w38DataGridViewTextBoxColumn.DataPropertyName = "W38";
		this.w38DataGridViewTextBoxColumn.HeaderText = "W38";
		this.w38DataGridViewTextBoxColumn.Name = "w38DataGridViewTextBoxColumn";
		this.w38DataGridViewTextBoxColumn.ReadOnly = true;
		this.w39DataGridViewTextBoxColumn.DataPropertyName = "W39";
		this.w39DataGridViewTextBoxColumn.HeaderText = "W39";
		this.w39DataGridViewTextBoxColumn.Name = "w39DataGridViewTextBoxColumn";
		this.w39DataGridViewTextBoxColumn.ReadOnly = true;
		this.w40DataGridViewTextBoxColumn.DataPropertyName = "W40";
		this.w40DataGridViewTextBoxColumn.HeaderText = "W40";
		this.w40DataGridViewTextBoxColumn.Name = "w40DataGridViewTextBoxColumn";
		this.w40DataGridViewTextBoxColumn.ReadOnly = true;
		this.w41DataGridViewTextBoxColumn.DataPropertyName = "W41";
		this.w41DataGridViewTextBoxColumn.HeaderText = "29 支付的其他与筹资活动有关的现金";
		this.w41DataGridViewTextBoxColumn.Name = "w41DataGridViewTextBoxColumn";
		this.w41DataGridViewTextBoxColumn.ReadOnly = true;
		this.w42DataGridViewTextBoxColumn.DataPropertyName = "W42";
		this.w42DataGridViewTextBoxColumn.HeaderText = "30 筹资活动现金流出小计";
		this.w42DataGridViewTextBoxColumn.Name = "w42DataGridViewTextBoxColumn";
		this.w42DataGridViewTextBoxColumn.ReadOnly = true;
		this.w43DataGridViewTextBoxColumn.DataPropertyName = "W43";
		this.w43DataGridViewTextBoxColumn.HeaderText = "31 筹资活动产生的现金流量净额";
		this.w43DataGridViewTextBoxColumn.Name = "w43DataGridViewTextBoxColumn";
		this.w43DataGridViewTextBoxColumn.ReadOnly = true;
		this.w44DataGridViewTextBoxColumn.DataPropertyName = "W44";
		this.w44DataGridViewTextBoxColumn.HeaderText = "32 汇率变动对现金及现金等价物的影响";
		this.w44DataGridViewTextBoxColumn.Name = "w44DataGridViewTextBoxColumn";
		this.w44DataGridViewTextBoxColumn.ReadOnly = true;
		this.w45DataGridViewTextBoxColumn.DataPropertyName = "W45";
		this.w45DataGridViewTextBoxColumn.HeaderText = "33 现金及现金等价物净增加额";
		this.w45DataGridViewTextBoxColumn.Name = "w45DataGridViewTextBoxColumn";
		this.w45DataGridViewTextBoxColumn.ReadOnly = true;
		this.w46DataGridViewTextBoxColumn.DataPropertyName = "W46";
		this.w46DataGridViewTextBoxColumn.HeaderText = "34 加：现金等价物的期末余额";
		this.w46DataGridViewTextBoxColumn.Name = "w46DataGridViewTextBoxColumn";
		this.w46DataGridViewTextBoxColumn.ReadOnly = true;
		this.w47DataGridViewTextBoxColumn.DataPropertyName = "W47";
		this.w47DataGridViewTextBoxColumn.HeaderText = "35 减：现金等价物的期初余额";
		this.w47DataGridViewTextBoxColumn.Name = "w47DataGridViewTextBoxColumn";
		this.w47DataGridViewTextBoxColumn.ReadOnly = true;
		this.mCashflowBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.CashflowRecord);
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
		this.positionDataGridViewTextBoxColumn.HeaderText = "开始下标";
		this.positionDataGridViewTextBoxColumn.Name = "positionDataGridViewTextBoxColumn";
		this.positionDataGridViewTextBoxColumn.ReadOnly = true;
		this.recordNumberDataGridViewTextBoxColumn.DataPropertyName = "RecordNumber";
		this.recordNumberDataGridViewTextBoxColumn.HeaderText = "隶属记录数";
		this.recordNumberDataGridViewTextBoxColumn.Name = "recordNumberDataGridViewTextBoxColumn";
		this.recordNumberDataGridViewTextBoxColumn.ReadOnly = true;
		this.mComplexBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.ComplexIndexRecord);
		this.mComplexBindingSource.PositionChanged += new System.EventHandler(OnComplexPositionChangedEvent);
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 473);
		base.Controls.Add(this.mContentView);
		base.Controls.Add(this.mSplitter);
		base.Controls.Add(this.mComplexView);
		base.Name = "CashflowUI";
		this.Text = "现金流量";
		((System.ComponentModel.ISupportInitialize)this.mContentView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mCashflowBindingSource).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).EndInit();
		base.ResumeLayout(false);
	}
}
