using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class DividendUI : Form
{
	private DividendFile m_File;

	private IContainer components;

	private DataGridView mContentView;

	private BindingSource mDividendBindingSource;

	private Splitter mSplitter;

	private BindingSource mComplexBindingSource;

	private DataGridView mComplexView;

	private DataGridViewTextBoxColumn marketDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn symbolDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn freeNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn positionDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn recordNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn dateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w1DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn exdividendDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn cashDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn splitDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn bonusDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn dispatchDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn priceDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn registerDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn listingDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn descriptionDataGridViewTextBoxColumn;

	public DividendUI()
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
			m_File = default(DividendFile);
			flag = DividendFile.Read(ref m_File, stream);
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
		mDividendBindingSource.SuspendBinding();
		try
		{
			mDividendBindingSource.Clear();
			ComplexIndexRecord complexIndexRecord = (ComplexIndexRecord)mComplexBindingSource[mComplexBindingSource.Position];
			for (int i = 0; i < complexIndexRecord.RecordNumber - complexIndexRecord.FreeNumber; i++)
			{
				if (m_File.RecordList[i + complexIndexRecord.Position].ExdividendDate > DateTime.MinValue)
				{
					mDividendBindingSource.Add(m_File.RecordList[i + complexIndexRecord.Position]);
				}
			}
			mDividendBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mDividendBindingSource.ResumeBinding();
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
		this.mContentView = new System.Windows.Forms.DataGridView();
		this.mSplitter = new System.Windows.Forms.Splitter();
		this.mComplexView = new System.Windows.Forms.DataGridView();
		this.dateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.w1DataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.exdividendDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.cashDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.splitDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.bonusDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.dispatchDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.priceDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.registerDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.listingDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.descriptionDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mDividendBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.marketDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.symbolDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.freeNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.positionDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.recordNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mComplexBindingSource = new System.Windows.Forms.BindingSource(this.components);
		((System.ComponentModel.ISupportInitialize)this.mContentView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mDividendBindingSource).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).BeginInit();
		base.SuspendLayout();
		this.mContentView.AllowUserToAddRows = false;
		this.mContentView.AllowUserToDeleteRows = false;
		this.mContentView.AutoGenerateColumns = false;
		this.mContentView.BackgroundColor = System.Drawing.SystemColors.Window;
		this.mContentView.BorderStyle = System.Windows.Forms.BorderStyle.None;
		this.mContentView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		this.mContentView.Columns.AddRange(this.dateDataGridViewTextBoxColumn, this.w1DataGridViewTextBoxColumn, this.exdividendDateDataGridViewTextBoxColumn, this.cashDataGridViewTextBoxColumn, this.splitDataGridViewTextBoxColumn, this.bonusDataGridViewTextBoxColumn, this.dispatchDataGridViewTextBoxColumn, this.priceDataGridViewTextBoxColumn, this.registerDateDataGridViewTextBoxColumn, this.listingDateDataGridViewTextBoxColumn, this.descriptionDataGridViewTextBoxColumn);
		this.mContentView.DataSource = this.mDividendBindingSource;
		this.mContentView.Dock = System.Windows.Forms.DockStyle.Fill;
		this.mContentView.Location = new System.Drawing.Point(303, 0);
		this.mContentView.Name = "mContentView";
		this.mContentView.ReadOnly = true;
		this.mContentView.RowHeadersVisible = false;
		this.mContentView.RowTemplate.Height = 20;
		this.mContentView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mContentView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mContentView.Size = new System.Drawing.Size(289, 473);
		this.mContentView.TabIndex = 2;
		this.mSplitter.Location = new System.Drawing.Point(300, 0);
		this.mSplitter.Name = "mSplitter";
		this.mSplitter.Size = new System.Drawing.Size(3, 473);
		this.mSplitter.TabIndex = 1;
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
		dataGridViewCellStyle.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		dataGridViewCellStyle.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.RowHeadersDefaultCellStyle = dataGridViewCellStyle;
		this.mComplexView.RowHeadersVisible = false;
		this.mComplexView.RowTemplate.Height = 20;
		this.mComplexView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mComplexView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mComplexView.Size = new System.Drawing.Size(300, 473);
		this.mComplexView.TabIndex = 0;
		this.dateDataGridViewTextBoxColumn.DataPropertyName = "Date";
		this.dateDataGridViewTextBoxColumn.HeaderText = "日期";
		this.dateDataGridViewTextBoxColumn.Name = "dateDataGridViewTextBoxColumn";
		this.dateDataGridViewTextBoxColumn.ReadOnly = true;
		this.w1DataGridViewTextBoxColumn.DataPropertyName = "W1";
		this.w1DataGridViewTextBoxColumn.HeaderText = "W1";
		this.w1DataGridViewTextBoxColumn.Name = "w1DataGridViewTextBoxColumn";
		this.w1DataGridViewTextBoxColumn.ReadOnly = true;
		this.exdividendDateDataGridViewTextBoxColumn.DataPropertyName = "ExdividendDate";
		this.exdividendDateDataGridViewTextBoxColumn.HeaderText = "除权日";
		this.exdividendDateDataGridViewTextBoxColumn.Name = "exdividendDateDataGridViewTextBoxColumn";
		this.exdividendDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.cashDataGridViewTextBoxColumn.DataPropertyName = "Cash";
		this.cashDataGridViewTextBoxColumn.HeaderText = "分红";
		this.cashDataGridViewTextBoxColumn.Name = "cashDataGridViewTextBoxColumn";
		this.cashDataGridViewTextBoxColumn.ReadOnly = true;
		this.splitDataGridViewTextBoxColumn.DataPropertyName = "Split";
		this.splitDataGridViewTextBoxColumn.HeaderText = "总拆股";
		this.splitDataGridViewTextBoxColumn.Name = "splitDataGridViewTextBoxColumn";
		this.splitDataGridViewTextBoxColumn.ReadOnly = true;
		this.bonusDataGridViewTextBoxColumn.DataPropertyName = "Bonus";
		this.bonusDataGridViewTextBoxColumn.HeaderText = "转增股";
		this.bonusDataGridViewTextBoxColumn.Name = "bonusDataGridViewTextBoxColumn";
		this.bonusDataGridViewTextBoxColumn.ReadOnly = true;
		this.dispatchDataGridViewTextBoxColumn.DataPropertyName = "Dispatch";
		this.dispatchDataGridViewTextBoxColumn.HeaderText = "配股";
		this.dispatchDataGridViewTextBoxColumn.Name = "dispatchDataGridViewTextBoxColumn";
		this.dispatchDataGridViewTextBoxColumn.ReadOnly = true;
		this.priceDataGridViewTextBoxColumn.DataPropertyName = "Price";
		this.priceDataGridViewTextBoxColumn.HeaderText = "配股价";
		this.priceDataGridViewTextBoxColumn.Name = "priceDataGridViewTextBoxColumn";
		this.priceDataGridViewTextBoxColumn.ReadOnly = true;
		this.registerDateDataGridViewTextBoxColumn.DataPropertyName = "RegisterDate";
		this.registerDateDataGridViewTextBoxColumn.HeaderText = "登记日";
		this.registerDateDataGridViewTextBoxColumn.Name = "registerDateDataGridViewTextBoxColumn";
		this.registerDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.listingDateDataGridViewTextBoxColumn.DataPropertyName = "ListingDate";
		this.listingDateDataGridViewTextBoxColumn.HeaderText = "上市日";
		this.listingDateDataGridViewTextBoxColumn.Name = "listingDateDataGridViewTextBoxColumn";
		this.listingDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.descriptionDataGridViewTextBoxColumn.DataPropertyName = "Description";
		this.descriptionDataGridViewTextBoxColumn.HeaderText = "描述";
		this.descriptionDataGridViewTextBoxColumn.Name = "descriptionDataGridViewTextBoxColumn";
		this.descriptionDataGridViewTextBoxColumn.ReadOnly = true;
		this.mDividendBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.DividendRecord);
		this.marketDataGridViewTextBoxColumn.DataPropertyName = "Market";
		this.marketDataGridViewTextBoxColumn.HeaderText = "市场";
		this.marketDataGridViewTextBoxColumn.Name = "marketDataGridViewTextBoxColumn";
		this.marketDataGridViewTextBoxColumn.ReadOnly = true;
		this.marketDataGridViewTextBoxColumn.Width = 60;
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
		base.Name = "DividendUI";
		this.Text = "权息";
		((System.ComponentModel.ISupportInitialize)this.mContentView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mDividendBindingSource).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).EndInit();
		base.ResumeLayout(false);
	}
}
