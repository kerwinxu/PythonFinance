using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class NegotiableUI : Form
{
	private NegotiableFile m_File;

	private IContainer components;

	private BindingSource mComplexBindingSource;

	private DataGridView mComplexView;

	private DataGridViewTextBoxColumn marketDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn symbolDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn freeNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn positionDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn recordNumberDataGridViewTextBoxColumn;

	private Splitter mSplitter;

	private DataGridView mContentView;

	private BindingSource mNegotiableBindingSource;

	private DataGridViewTextBoxColumn dateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn exdividendDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn splitDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn cashDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn warrantsExerciseNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn warrantsExercisePriceDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn warrantsBonusDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn putWarrantsExerciseNumberDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn putWarrantsExercisePriceDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn putWarrantsBonusDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn nonNegotiableShrinkDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn registerDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn operateDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn listingDateDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn reformSchemeDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn periodOfExistenceDataGridViewTextBoxColumn;

	public NegotiableUI()
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
			m_File = default(NegotiableFile);
			flag = NegotiableFile.Read(ref m_File, stream);
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
		mNegotiableBindingSource.SuspendBinding();
		try
		{
			mNegotiableBindingSource.Clear();
			ComplexIndexRecord complexIndexRecord = (ComplexIndexRecord)mComplexBindingSource[mComplexBindingSource.Position];
			for (int i = 0; i < complexIndexRecord.RecordNumber - complexIndexRecord.FreeNumber; i++)
			{
				mNegotiableBindingSource.Add(m_File.RecordList[i + complexIndexRecord.Position]);
			}
			mNegotiableBindingSource.ResetBindings(metadataChanged: false);
		}
		finally
		{
			mNegotiableBindingSource.ResumeBinding();
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
		this.mComplexView = new System.Windows.Forms.DataGridView();
		this.marketDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.symbolDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.freeNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.positionDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.recordNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mComplexBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.mSplitter = new System.Windows.Forms.Splitter();
		this.mContentView = new System.Windows.Forms.DataGridView();
		this.dateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.exdividendDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.splitDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.cashDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.warrantsExerciseNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.warrantsExercisePriceDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.warrantsBonusDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.putWarrantsExerciseNumberDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.putWarrantsExercisePriceDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.putWarrantsBonusDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.nonNegotiableShrinkDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.registerDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.operateDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.listingDateDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.reformSchemeDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.periodOfExistenceDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.mNegotiableBindingSource = new System.Windows.Forms.BindingSource(this.components);
		((System.ComponentModel.ISupportInitialize)this.mComplexView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mContentView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mNegotiableBindingSource).BeginInit();
		base.SuspendLayout();
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
		this.mComplexView.RowHeadersVisible = false;
		this.mComplexView.RowTemplate.Height = 23;
		this.mComplexView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mComplexView.Size = new System.Drawing.Size(300, 473);
		this.mComplexView.TabIndex = 0;
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
		this.mSplitter.Location = new System.Drawing.Point(300, 0);
		this.mSplitter.Name = "mSplitter";
		this.mSplitter.Size = new System.Drawing.Size(3, 473);
		this.mSplitter.TabIndex = 1;
		this.mSplitter.TabStop = false;
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
		this.mContentView.Columns.AddRange(this.dateDataGridViewTextBoxColumn, this.exdividendDateDataGridViewTextBoxColumn, this.splitDataGridViewTextBoxColumn, this.cashDataGridViewTextBoxColumn, this.warrantsExerciseNumberDataGridViewTextBoxColumn, this.warrantsExercisePriceDataGridViewTextBoxColumn, this.warrantsBonusDataGridViewTextBoxColumn, this.putWarrantsExerciseNumberDataGridViewTextBoxColumn, this.putWarrantsExercisePriceDataGridViewTextBoxColumn, this.putWarrantsBonusDataGridViewTextBoxColumn, this.nonNegotiableShrinkDataGridViewTextBoxColumn, this.registerDateDataGridViewTextBoxColumn, this.operateDateDataGridViewTextBoxColumn, this.listingDateDataGridViewTextBoxColumn, this.reformSchemeDataGridViewTextBoxColumn, this.periodOfExistenceDataGridViewTextBoxColumn);
		this.mContentView.DataSource = this.mNegotiableBindingSource;
		this.mContentView.Dock = System.Windows.Forms.DockStyle.Fill;
		this.mContentView.Location = new System.Drawing.Point(303, 0);
		this.mContentView.Name = "mContentView";
		this.mContentView.ReadOnly = true;
		this.mContentView.RowHeadersVisible = false;
		this.mContentView.RowTemplate.Height = 23;
		this.mContentView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mContentView.Size = new System.Drawing.Size(289, 473);
		this.mContentView.TabIndex = 2;
		this.dateDataGridViewTextBoxColumn.DataPropertyName = "Date";
		this.dateDataGridViewTextBoxColumn.HeaderText = "日期";
		this.dateDataGridViewTextBoxColumn.Name = "dateDataGridViewTextBoxColumn";
		this.dateDataGridViewTextBoxColumn.ReadOnly = true;
		this.exdividendDateDataGridViewTextBoxColumn.DataPropertyName = "ExdividendDate";
		this.exdividendDateDataGridViewTextBoxColumn.HeaderText = "除息日";
		this.exdividendDateDataGridViewTextBoxColumn.Name = "exdividendDateDataGridViewTextBoxColumn";
		this.exdividendDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.splitDataGridViewTextBoxColumn.DataPropertyName = "Split";
		this.splitDataGridViewTextBoxColumn.HeaderText = "送股";
		this.splitDataGridViewTextBoxColumn.Name = "splitDataGridViewTextBoxColumn";
		this.splitDataGridViewTextBoxColumn.ReadOnly = true;
		this.cashDataGridViewTextBoxColumn.DataPropertyName = "Cash";
		this.cashDataGridViewTextBoxColumn.HeaderText = "现金";
		this.cashDataGridViewTextBoxColumn.Name = "cashDataGridViewTextBoxColumn";
		this.cashDataGridViewTextBoxColumn.ReadOnly = true;
		this.warrantsExerciseNumberDataGridViewTextBoxColumn.DataPropertyName = "WarrantsExerciseNumber";
		this.warrantsExerciseNumberDataGridViewTextBoxColumn.HeaderText = "认购权证行权比例";
		this.warrantsExerciseNumberDataGridViewTextBoxColumn.Name = "warrantsExerciseNumberDataGridViewTextBoxColumn";
		this.warrantsExerciseNumberDataGridViewTextBoxColumn.ReadOnly = true;
		this.warrantsExercisePriceDataGridViewTextBoxColumn.DataPropertyName = "WarrantsExercisePrice";
		this.warrantsExercisePriceDataGridViewTextBoxColumn.HeaderText = "认购权证行权价格";
		this.warrantsExercisePriceDataGridViewTextBoxColumn.Name = "warrantsExercisePriceDataGridViewTextBoxColumn";
		this.warrantsExercisePriceDataGridViewTextBoxColumn.ReadOnly = true;
		this.warrantsBonusDataGridViewTextBoxColumn.DataPropertyName = "WarrantsBonus";
		this.warrantsBonusDataGridViewTextBoxColumn.HeaderText = "赠送认购权证份数";
		this.warrantsBonusDataGridViewTextBoxColumn.Name = "warrantsBonusDataGridViewTextBoxColumn";
		this.warrantsBonusDataGridViewTextBoxColumn.ReadOnly = true;
		this.putWarrantsExerciseNumberDataGridViewTextBoxColumn.DataPropertyName = "PutWarrantsExerciseNumber";
		this.putWarrantsExerciseNumberDataGridViewTextBoxColumn.HeaderText = "认沽权证行权比例";
		this.putWarrantsExerciseNumberDataGridViewTextBoxColumn.Name = "putWarrantsExerciseNumberDataGridViewTextBoxColumn";
		this.putWarrantsExerciseNumberDataGridViewTextBoxColumn.ReadOnly = true;
		this.putWarrantsExercisePriceDataGridViewTextBoxColumn.DataPropertyName = "PutWarrantsExercisePrice";
		this.putWarrantsExercisePriceDataGridViewTextBoxColumn.HeaderText = "认沽权证行权价格";
		this.putWarrantsExercisePriceDataGridViewTextBoxColumn.Name = "putWarrantsExercisePriceDataGridViewTextBoxColumn";
		this.putWarrantsExercisePriceDataGridViewTextBoxColumn.ReadOnly = true;
		this.putWarrantsBonusDataGridViewTextBoxColumn.DataPropertyName = "PutWarrantsBonus";
		this.putWarrantsBonusDataGridViewTextBoxColumn.HeaderText = "赠送认沽权证份数";
		this.putWarrantsBonusDataGridViewTextBoxColumn.Name = "putWarrantsBonusDataGridViewTextBoxColumn";
		this.putWarrantsBonusDataGridViewTextBoxColumn.ReadOnly = true;
		this.nonNegotiableShrinkDataGridViewTextBoxColumn.DataPropertyName = "NonNegotiableShrink";
		this.nonNegotiableShrinkDataGridViewTextBoxColumn.HeaderText = "非流通股缩股";
		this.nonNegotiableShrinkDataGridViewTextBoxColumn.Name = "nonNegotiableShrinkDataGridViewTextBoxColumn";
		this.nonNegotiableShrinkDataGridViewTextBoxColumn.ReadOnly = true;
		this.registerDateDataGridViewTextBoxColumn.DataPropertyName = "RegisterDate";
		this.registerDateDataGridViewTextBoxColumn.HeaderText = "登记日";
		this.registerDateDataGridViewTextBoxColumn.Name = "registerDateDataGridViewTextBoxColumn";
		this.registerDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.operateDateDataGridViewTextBoxColumn.DataPropertyName = "OperateDate";
		this.operateDateDataGridViewTextBoxColumn.HeaderText = "实施日";
		this.operateDateDataGridViewTextBoxColumn.Name = "operateDateDataGridViewTextBoxColumn";
		this.operateDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.listingDateDataGridViewTextBoxColumn.DataPropertyName = "ListingDate";
		this.listingDateDataGridViewTextBoxColumn.HeaderText = "上市日";
		this.listingDateDataGridViewTextBoxColumn.Name = "listingDateDataGridViewTextBoxColumn";
		this.listingDateDataGridViewTextBoxColumn.ReadOnly = true;
		this.reformSchemeDataGridViewTextBoxColumn.DataPropertyName = "ReformScheme";
		this.reformSchemeDataGridViewTextBoxColumn.HeaderText = "股改方案";
		this.reformSchemeDataGridViewTextBoxColumn.Name = "reformSchemeDataGridViewTextBoxColumn";
		this.reformSchemeDataGridViewTextBoxColumn.ReadOnly = true;
		this.periodOfExistenceDataGridViewTextBoxColumn.DataPropertyName = "PeriodOfExistence";
		this.periodOfExistenceDataGridViewTextBoxColumn.HeaderText = "存续期说明";
		this.periodOfExistenceDataGridViewTextBoxColumn.Name = "periodOfExistenceDataGridViewTextBoxColumn";
		this.periodOfExistenceDataGridViewTextBoxColumn.ReadOnly = true;
		this.mNegotiableBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.NegotiableRecord);
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 473);
		base.Controls.Add(this.mContentView);
		base.Controls.Add(this.mSplitter);
		base.Controls.Add(this.mComplexView);
		base.Name = "NegotiableUI";
		this.Text = "全流通";
		((System.ComponentModel.ISupportInitialize)this.mComplexView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mComplexBindingSource).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mContentView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mNegotiableBindingSource).EndInit();
		base.ResumeLayout(false);
	}
}
