using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class AnnotationUI : Form
{
	private IContainer components;

	private DataGridView mContentView;

	private BindingSource mAnnotationBindingSource;

	private Splitter mSplitter;

	private DataGridView mComplexView;

	private DataGridViewTextBoxColumn marketDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn symbolDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn freeNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn positionDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn recordNumberDataGridViewTextBoxColumn;

	private BindingSource mComplexBindingSource;

	private DataGridViewTextBoxColumn dateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w1DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w2DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w3DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w4DataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn w5DataGridViewTextBoxColumn;

	private AnnotationFile m_File;

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
		this.mAnnotationBindingSource = new System.Windows.Forms.BindingSource(this.components);
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
		((System.ComponentModel.ISupportInitialize)this.mContentView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mAnnotationBindingSource).BeginInit();
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
		this.mContentView.Columns.AddRange(this.dateDataGridViewTextBoxColumn, this.w1DataGridViewTextBoxColumn, this.w2DataGridViewTextBoxColumn, this.w3DataGridViewTextBoxColumn, this.w4DataGridViewTextBoxColumn, this.w5DataGridViewTextBoxColumn);
		this.mContentView.DataSource = this.mAnnotationBindingSource;
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
		this.mComplexView.TabIndex = 6;
		this.mAnnotationBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.AnnotationRecord);
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
		this.mComplexBindingSource.CurrentChanged += new System.EventHandler(OnComplexPositionChangedEvent);
		this.dateDataGridViewTextBoxColumn.DataPropertyName = "Date";
		this.dateDataGridViewTextBoxColumn.HeaderText = "日期";
		this.dateDataGridViewTextBoxColumn.Name = "dateDataGridViewTextBoxColumn";
		this.dateDataGridViewTextBoxColumn.ReadOnly = true;
		this.w1DataGridViewTextBoxColumn.DataPropertyName = "W1";
		this.w1DataGridViewTextBoxColumn.HeaderText = "W1";
		this.w1DataGridViewTextBoxColumn.Name = "w1DataGridViewTextBoxColumn";
		this.w1DataGridViewTextBoxColumn.ReadOnly = true;
		this.w2DataGridViewTextBoxColumn.DataPropertyName = "W2";
		this.w2DataGridViewTextBoxColumn.HeaderText = "基本每股收益(元)";
		this.w2DataGridViewTextBoxColumn.Name = "w2DataGridViewTextBoxColumn";
		this.w2DataGridViewTextBoxColumn.ReadOnly = true;
		this.w3DataGridViewTextBoxColumn.DataPropertyName = "W3";
		this.w3DataGridViewTextBoxColumn.HeaderText = "净资产收益率(%)";
		this.w3DataGridViewTextBoxColumn.Name = "w3DataGridViewTextBoxColumn";
		this.w3DataGridViewTextBoxColumn.ReadOnly = true;
		this.w4DataGridViewTextBoxColumn.DataPropertyName = "W4";
		this.w4DataGridViewTextBoxColumn.HeaderText = "每股净资产(元)";
		this.w4DataGridViewTextBoxColumn.Name = "w4DataGridViewTextBoxColumn";
		this.w4DataGridViewTextBoxColumn.ReadOnly = true;
		this.w5DataGridViewTextBoxColumn.DataPropertyName = "W5";
		this.w5DataGridViewTextBoxColumn.HeaderText = "净利润";
		this.w5DataGridViewTextBoxColumn.Name = "w5DataGridViewTextBoxColumn";
		this.w5DataGridViewTextBoxColumn.ReadOnly = true;
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 473);
		base.Controls.Add(this.mContentView);
		base.Controls.Add(this.mSplitter);
		base.Controls.Add(this.mComplexView);
		base.Name = "AnnotationUI";
		this.Text = "财务附注";
		((System.ComponentModel.ISupportInitialize)this.mContentView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mAnnotationBindingSource).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).EndInit();
		base.ResumeLayout(false);
	}

	public AnnotationUI()
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
			m_File = default(AnnotationFile);
			flag = AnnotationFile.Read(ref m_File, stream);
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
		mAnnotationBindingSource.SuspendBinding();
		try
		{
			mAnnotationBindingSource.Clear();
			ComplexIndexRecord complexIndexRecord = (ComplexIndexRecord)mComplexBindingSource[mComplexBindingSource.Position];
			for (int i = 0; i < complexIndexRecord.RecordNumber; i++)
			{
				if (m_File.RecordList[i + complexIndexRecord.Position].Date > DateTime.MinValue)
				{
					mAnnotationBindingSource.Add(m_File.RecordList[i + complexIndexRecord.Position]);
				}
			}
			mAnnotationBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mAnnotationBindingSource.ResumeBinding();
		}
	}
}
