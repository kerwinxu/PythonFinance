using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class D1BarUI : Form
{
	private IContainer components;

	private BindingSource mBindingSource;

	private DataGridView mDataView;

	private DataGridViewTextBoxColumn dataGridViewTextBoxColumn1;

	private DataGridViewTextBoxColumn openDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn highDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn lowDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn closeDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn amountDataGridViewTextBoxColumn;

	private DataGridViewTextBoxColumn volumeDataGridViewTextBoxColumn;

	public D1BarUI()
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
		D1BarFile file = default(D1BarFile);
		bool flag = false;
		using (FileStream stream = File.OpenRead(filename))
		{
			flag = D1BarFile.Read(ref file, stream);
		}
		if (!flag)
		{
			return;
		}
		mBindingSource.SuspendBinding();
		try
		{
			mBindingSource.Clear();
			D1BarRecord[] recordList = file.RecordList;
			foreach (D1BarRecord d1BarRecord in recordList)
			{
				mBindingSource.Add(d1BarRecord);
			}
		}
		finally
		{
			mBindingSource.ResumeBinding();
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
		this.mDataView = new System.Windows.Forms.DataGridView();
		this.mBindingSource = new System.Windows.Forms.BindingSource(this.components);
		this.dataGridViewTextBoxColumn1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.openDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.highDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.lowDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.closeDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.amountDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		this.volumeDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
		((System.ComponentModel.ISupportInitialize)this.mDataView).BeginInit();
		((System.ComponentModel.ISupportInitialize)this.mBindingSource).BeginInit();
		base.SuspendLayout();
		this.mDataView.AllowUserToAddRows = false;
		this.mDataView.AllowUserToDeleteRows = false;
		this.mDataView.AutoGenerateColumns = false;
		this.mDataView.BackgroundColor = System.Drawing.SystemColors.Window;
		dataGridViewCellStyle.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
		dataGridViewCellStyle.BackColor = System.Drawing.SystemColors.Control;
		dataGridViewCellStyle.Font = new System.Drawing.Font("宋体", 9f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134);
		dataGridViewCellStyle.ForeColor = System.Drawing.SystemColors.WindowText;
		dataGridViewCellStyle.SelectionBackColor = System.Drawing.SystemColors.Highlight;
		dataGridViewCellStyle.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
		this.mDataView.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle;
		this.mDataView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		this.mDataView.Columns.AddRange(this.dataGridViewTextBoxColumn1, this.openDataGridViewTextBoxColumn, this.highDataGridViewTextBoxColumn, this.lowDataGridViewTextBoxColumn, this.closeDataGridViewTextBoxColumn, this.amountDataGridViewTextBoxColumn, this.volumeDataGridViewTextBoxColumn);
		this.mDataView.DataSource = this.mBindingSource;
		this.mDataView.Dock = System.Windows.Forms.DockStyle.Fill;
		this.mDataView.Location = new System.Drawing.Point(0, 0);
		this.mDataView.Name = "mDataView";
		this.mDataView.ReadOnly = true;
		this.mDataView.RowHeadersVisible = false;
		this.mDataView.RowTemplate.Height = 20;
		this.mDataView.RowTemplate.Resizable = System.Windows.Forms.DataGridViewTriState.False;
		this.mDataView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
		this.mDataView.Size = new System.Drawing.Size(592, 473);
		this.mDataView.TabIndex = 0;
		this.mBindingSource.DataSource = typeof(Oci.Athena.DataSource.Hexin.D1BarRecord);
		this.dataGridViewTextBoxColumn1.DataPropertyName = "Date";
		this.dataGridViewTextBoxColumn1.HeaderText = "日期";
		this.dataGridViewTextBoxColumn1.Name = "dataGridViewTextBoxColumn1";
		this.dataGridViewTextBoxColumn1.ReadOnly = true;
		this.openDataGridViewTextBoxColumn.DataPropertyName = "Open";
		this.openDataGridViewTextBoxColumn.HeaderText = "开盘价";
		this.openDataGridViewTextBoxColumn.Name = "openDataGridViewTextBoxColumn";
		this.openDataGridViewTextBoxColumn.ReadOnly = true;
		this.highDataGridViewTextBoxColumn.DataPropertyName = "High";
		this.highDataGridViewTextBoxColumn.HeaderText = "最高价";
		this.highDataGridViewTextBoxColumn.Name = "highDataGridViewTextBoxColumn";
		this.highDataGridViewTextBoxColumn.ReadOnly = true;
		this.lowDataGridViewTextBoxColumn.DataPropertyName = "Low";
		this.lowDataGridViewTextBoxColumn.HeaderText = "最低价";
		this.lowDataGridViewTextBoxColumn.Name = "lowDataGridViewTextBoxColumn";
		this.lowDataGridViewTextBoxColumn.ReadOnly = true;
		this.closeDataGridViewTextBoxColumn.DataPropertyName = "Close";
		this.closeDataGridViewTextBoxColumn.HeaderText = "收盘价";
		this.closeDataGridViewTextBoxColumn.Name = "closeDataGridViewTextBoxColumn";
		this.closeDataGridViewTextBoxColumn.ReadOnly = true;
		this.amountDataGridViewTextBoxColumn.DataPropertyName = "Amount";
		this.amountDataGridViewTextBoxColumn.HeaderText = "成交金额";
		this.amountDataGridViewTextBoxColumn.Name = "amountDataGridViewTextBoxColumn";
		this.amountDataGridViewTextBoxColumn.ReadOnly = true;
		this.volumeDataGridViewTextBoxColumn.DataPropertyName = "Volume";
		this.volumeDataGridViewTextBoxColumn.HeaderText = "成交量";
		this.volumeDataGridViewTextBoxColumn.Name = "volumeDataGridViewTextBoxColumn";
		this.volumeDataGridViewTextBoxColumn.ReadOnly = true;
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 473);
		base.Controls.Add(this.mDataView);
		base.Name = "D1BarUI";
		this.Text = "日线文件";
		((System.ComponentModel.ISupportInitialize)this.mDataView).EndInit();
		((System.ComponentModel.ISupportInitialize)this.mBindingSource).EndInit();
		base.ResumeLayout(false);
	}
}
