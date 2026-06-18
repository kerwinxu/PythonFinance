using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace Oci.Athena.DataSource.Hexin.DataViewer;

public class HomeUI : Form
{
	private IContainer components;

	private MenuStrip mMenuStrip;

	private ToolStripMenuItem mFileMenu;

	private ToolStripMenuItem mOpenMenu;

	private ToolStripMenuItem mOpenD1BarMenu;

	private OpenFileDialog mOpenD1BarDialog;

	private ToolStripMenuItem mOpenDividendMenu;

	private OpenFileDialog mOpenDividendDialog;

	private ToolStripSeparator mOpenSeparator;

	private ToolStripMenuItem mExitMenu;

	private ToolStripMenuItem mWindowMenu;

	private ToolStripMenuItem mOpenNegotiableMenu;

	private OpenFileDialog mOpenNegotiableDialog;

	private ToolStripMenuItem mOpenCashflowMenu;

	private OpenFileDialog mOpenCashflowDialog;

	private ToolStripMenuItem mOpenBalanceMenu;

	private OpenFileDialog mOpenBalanceDialog;

	private ToolStripMenuItem mOpenProfitMenu;

	private OpenFileDialog mOpenProfitDialog;

	private ToolStripMenuItem mOpenInformationMenu;

	private OpenFileDialog mOpenInformationDialog;

	private ToolStripMenuItem mOpenAnnotationMenu;

	private OpenFileDialog mOpenAnnotationDialog;

	private ToolStripMenuItem mOpenIssueMenu;

	private OpenFileDialog mOpenIssueDialog;

	private ToolStripMenuItem mOpenCapitalMenu;

	private OpenFileDialog mOpenEquityDialog;

	private OpenFileDialog mOpenCapitalistDialog;

	private ToolStripMenuItem mOpenCapitalistMenu;

	private ToolStripMenuItem mOpenStockholderMenu;

	private OpenFileDialog mOpenStockholderDialog;

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
		this.mMenuStrip = new System.Windows.Forms.MenuStrip();
		this.mFileMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenD1BarMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenDividendMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenNegotiableMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenCashflowMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenBalanceMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenProfitMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenInformationMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenAnnotationMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenIssueMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenCapitalMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenSeparator = new System.Windows.Forms.ToolStripSeparator();
		this.mExitMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mWindowMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenD1BarDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenDividendDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenNegotiableDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenCashflowDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenBalanceDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenProfitDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenInformationDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenAnnotationDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenIssueDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenEquityDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenCapitalistDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenCapitalistMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mOpenStockholderDialog = new System.Windows.Forms.OpenFileDialog();
		this.mOpenStockholderMenu = new System.Windows.Forms.ToolStripMenuItem();
		this.mMenuStrip.SuspendLayout();
		base.SuspendLayout();
		this.mMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[2] { this.mFileMenu, this.mWindowMenu });
		this.mMenuStrip.Location = new System.Drawing.Point(0, 0);
		this.mMenuStrip.MdiWindowListItem = this.mWindowMenu;
		this.mMenuStrip.Name = "mMenuStrip";
		this.mMenuStrip.Size = new System.Drawing.Size(592, 24);
		this.mMenuStrip.TabIndex = 0;
		this.mMenuStrip.Text = "菜单栏";
		this.mFileMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[3] { this.mOpenMenu, this.mOpenSeparator, this.mExitMenu });
		this.mFileMenu.MergeAction = System.Windows.Forms.MergeAction.MatchOnly;
		this.mFileMenu.MergeIndex = 100;
		this.mFileMenu.Name = "mFileMenu";
		this.mFileMenu.Size = new System.Drawing.Size(59, 20);
		this.mFileMenu.Text = "文件(&F)";
		this.mOpenMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[12]
		{
			this.mOpenD1BarMenu, this.mOpenDividendMenu, this.mOpenNegotiableMenu, this.mOpenCashflowMenu, this.mOpenBalanceMenu, this.mOpenProfitMenu, this.mOpenInformationMenu, this.mOpenAnnotationMenu, this.mOpenIssueMenu, this.mOpenCapitalMenu,
			this.mOpenCapitalistMenu, this.mOpenStockholderMenu
		});
		this.mOpenMenu.Name = "mOpenMenu";
		this.mOpenMenu.Size = new System.Drawing.Size(152, 22);
		this.mOpenMenu.Text = "打开";
		this.mOpenD1BarMenu.Name = "mOpenD1BarMenu";
		this.mOpenD1BarMenu.ShortcutKeys = System.Windows.Forms.Keys.D | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenD1BarMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenD1BarMenu.Text = "日线行情(&D)";
		this.mOpenD1BarMenu.Click += new System.EventHandler(OnOpenD1BarClick);
		this.mOpenDividendMenu.Name = "mOpenDividendMenu";
		this.mOpenDividendMenu.ShortcutKeys = System.Windows.Forms.Keys.I | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenDividendMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenDividendMenu.Text = "权息(&I)";
		this.mOpenDividendMenu.Click += new System.EventHandler(OnOpenDividendClick);
		this.mOpenNegotiableMenu.Name = "mOpenNegotiableMenu";
		this.mOpenNegotiableMenu.ShortcutKeys = System.Windows.Forms.Keys.N | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenNegotiableMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenNegotiableMenu.Text = "全流通对价(&N)";
		this.mOpenNegotiableMenu.Click += new System.EventHandler(OnOpenNegotiableClick);
		this.mOpenCashflowMenu.Name = "mOpenCashflowMenu";
		this.mOpenCashflowMenu.ShortcutKeys = System.Windows.Forms.Keys.C | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenCashflowMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenCashflowMenu.Text = "现金流量(&C)";
		this.mOpenCashflowMenu.Click += new System.EventHandler(OnOpenCashflowClick);
		this.mOpenBalanceMenu.Name = "mOpenBalanceMenu";
		this.mOpenBalanceMenu.ShortcutKeys = System.Windows.Forms.Keys.B | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenBalanceMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenBalanceMenu.Text = "资产负债(&B)";
		this.mOpenBalanceMenu.Click += new System.EventHandler(OnOpenBalanceClick);
		this.mOpenProfitMenu.Name = "mOpenProfitMenu";
		this.mOpenProfitMenu.ShortcutKeys = System.Windows.Forms.Keys.P | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenProfitMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenProfitMenu.Text = "利润分配(&P)";
		this.mOpenProfitMenu.Click += new System.EventHandler(OnOpenProfitClick);
		this.mOpenInformationMenu.Name = "mOpenInformationMenu";
		this.mOpenInformationMenu.ShortcutKeys = System.Windows.Forms.Keys.I | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenInformationMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenInformationMenu.Text = "基本信息(&I)";
		this.mOpenInformationMenu.Click += new System.EventHandler(OnOpenInformationClick);
		this.mOpenAnnotationMenu.Name = "mOpenAnnotationMenu";
		this.mOpenAnnotationMenu.ShortcutKeys = System.Windows.Forms.Keys.A | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenAnnotationMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenAnnotationMenu.Text = "财务附注(&A)";
		this.mOpenAnnotationMenu.Click += new System.EventHandler(OnOpenAnnotationClick);
		this.mOpenIssueMenu.Name = "mOpenIssueMenu";
		this.mOpenIssueMenu.ShortcutKeys = System.Windows.Forms.Keys.U | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenIssueMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenIssueMenu.Text = "发行上市(&U)";
		this.mOpenIssueMenu.Click += new System.EventHandler(OnOpenIssueClick);
		this.mOpenCapitalMenu.Name = "mOpenCapitalMenu";
		this.mOpenCapitalMenu.ShortcutKeys = System.Windows.Forms.Keys.T | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenCapitalMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenCapitalMenu.Text = "股本结构(&T)";
		this.mOpenCapitalMenu.Click += new System.EventHandler(OnOpenCapitalClick);
		this.mOpenSeparator.Name = "mOpenSeparator";
		this.mOpenSeparator.Size = new System.Drawing.Size(149, 6);
		this.mExitMenu.Name = "mExitMenu";
		this.mExitMenu.Size = new System.Drawing.Size(152, 22);
		this.mExitMenu.Text = "退出(&X)";
		this.mExitMenu.Click += new System.EventHandler(OnExitClick);
		this.mWindowMenu.MergeAction = System.Windows.Forms.MergeAction.MatchOnly;
		this.mWindowMenu.MergeIndex = 9000;
		this.mWindowMenu.Name = "mWindowMenu";
		this.mWindowMenu.Size = new System.Drawing.Size(59, 20);
		this.mWindowMenu.Text = "窗口(&W)";
		this.mOpenD1BarDialog.DefaultExt = "DAY";
		this.mOpenD1BarDialog.Filter = "日线文件 (*.DAY)|*.DAY|所有文件 (*.*)|*.*";
		this.mOpenDividendDialog.DefaultExt = "财经";
		this.mOpenDividendDialog.Filter = "权息资料.财经|权息资料.财经|所有文件 (*.*)|*.*";
		this.mOpenNegotiableDialog.DefaultExt = "财经";
		this.mOpenNegotiableDialog.Filter = "全流通.财经|全流通.财经|所有文件 (*.*)|*.*";
		this.mOpenCashflowDialog.DefaultExt = "财经";
		this.mOpenCashflowDialog.Filter = "现金流量.财经|现金流量.财经|所有文件 (*.*)|*.*";
		this.mOpenBalanceDialog.DefaultExt = "财经";
		this.mOpenBalanceDialog.Filter = "资产负债.财经|资产负债.财经|所有文件 (*.*)|*.*";
		this.mOpenProfitDialog.DefaultExt = "财经";
		this.mOpenProfitDialog.Filter = "利润分配.财经|利润分配.财经|所有文件 (*.*)|*.*";
		this.mOpenInformationDialog.DefaultExt = "财经";
		this.mOpenInformationDialog.Filter = "基本信息.财经|基本信息.财经|所有文件 (*.*)|*.*";
		this.mOpenAnnotationDialog.DefaultExt = "财经";
		this.mOpenAnnotationDialog.Filter = "财务附注.财经|财务附注.财经|所有文件 (*.*)|*.*";
		this.mOpenIssueDialog.DefaultExt = "财经";
		this.mOpenIssueDialog.Filter = "发行上市.财经|发行上市.财经|所有文件 (*.*)|*.*";
		this.mOpenEquityDialog.DefaultExt = "财经";
		this.mOpenEquityDialog.Filter = "股本结构.财经|股本结构.财经|所有文件 (*.*)|*.*";
		this.mOpenCapitalistDialog.DefaultExt = "财经";
		this.mOpenCapitalistDialog.Filter = "十大股东.财经|十大股东.财经|所有文件 (*.*)|*.*";
		this.mOpenCapitalistMenu.Name = "mOpenCapitalistMenu";
		this.mOpenCapitalistMenu.ShortcutKeys = System.Windows.Forms.Keys.L | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenCapitalistMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenCapitalistMenu.Text = "十大股东(&L)";
		this.mOpenCapitalistMenu.Click += new System.EventHandler(OnOpenCapitalistClick);
		this.mOpenStockholderDialog.DefaultExt = "财经";
		this.mOpenStockholderDialog.Filter = "十大流通股东.财经|十大流通股东.财经|所有文件 (*.*)|*.*";
		this.mOpenStockholderMenu.Name = "mOpenStockholderMenu";
		this.mOpenStockholderMenu.ShortcutKeys = System.Windows.Forms.Keys.H | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.Control;
		this.mOpenStockholderMenu.Size = new System.Drawing.Size(237, 22);
		this.mOpenStockholderMenu.Text = "十大流通股东(&H)";
		this.mOpenStockholderMenu.Click += new System.EventHandler(OnOpenStockholderClick);
		base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
		base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
		base.ClientSize = new System.Drawing.Size(592, 423);
		base.Controls.Add(this.mMenuStrip);
		base.IsMdiContainer = true;
		base.MainMenuStrip = this.mMenuStrip;
		base.Name = "HomeUI";
		base.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
		this.Text = "同花顺数据阅读器";
		this.mMenuStrip.ResumeLayout(false);
		this.mMenuStrip.PerformLayout();
		base.ResumeLayout(false);
		base.PerformLayout();
	}

	public HomeUI()
	{
		InitializeComponent();
	}

	private void OnOpenD1BarClick(object sender, EventArgs e)
	{
		if (mOpenD1BarDialog.ShowDialog() == DialogResult.OK)
		{
			D1BarUI d1BarUI = new D1BarUI();
			d1BarUI.MdiParent = this;
			d1BarUI.Initialize(mOpenD1BarDialog.FileName);
			d1BarUI.Show();
			d1BarUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenDividendClick(object sender, EventArgs e)
	{
		if (mOpenDividendDialog.ShowDialog() == DialogResult.OK)
		{
			DividendUI dividendUI = new DividendUI();
			dividendUI.MdiParent = this;
			dividendUI.Initialize(mOpenDividendDialog.FileName);
			dividendUI.Show();
			dividendUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnExitClick(object sender, EventArgs e)
	{
		Application.Exit();
	}

	private void OnOpenNegotiableClick(object sender, EventArgs e)
	{
		if (mOpenNegotiableDialog.ShowDialog() == DialogResult.OK)
		{
			NegotiableUI negotiableUI = new NegotiableUI();
			negotiableUI.MdiParent = this;
			negotiableUI.Initialize(mOpenNegotiableDialog.FileName);
			negotiableUI.Show();
			negotiableUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenCashflowClick(object sender, EventArgs e)
	{
		if (mOpenCashflowDialog.ShowDialog() == DialogResult.OK)
		{
			CashflowUI cashflowUI = new CashflowUI();
			cashflowUI.MdiParent = this;
			cashflowUI.Initialize(mOpenCashflowDialog.FileName);
			cashflowUI.Show();
			cashflowUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenBalanceClick(object sender, EventArgs e)
	{
		if (mOpenBalanceDialog.ShowDialog() == DialogResult.OK)
		{
			BalanceUI balanceUI = new BalanceUI();
			balanceUI.MdiParent = this;
			balanceUI.Initialize(mOpenBalanceDialog.FileName);
			balanceUI.Show();
			balanceUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenProfitClick(object sender, EventArgs e)
	{
		if (mOpenProfitDialog.ShowDialog() == DialogResult.OK)
		{
			ProfitUI profitUI = new ProfitUI();
			profitUI.MdiParent = this;
			profitUI.Initialize(mOpenProfitDialog.FileName);
			profitUI.Show();
			profitUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenInformationClick(object sender, EventArgs e)
	{
		if (mOpenInformationDialog.ShowDialog() == DialogResult.OK)
		{
			InformationUI informationUI = new InformationUI();
			informationUI.MdiParent = this;
			informationUI.Initialize(mOpenInformationDialog.FileName);
			informationUI.Show();
			informationUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenAnnotationClick(object sender, EventArgs e)
	{
		if (mOpenAnnotationDialog.ShowDialog() == DialogResult.OK)
		{
			AnnotationUI annotationUI = new AnnotationUI();
			annotationUI.MdiParent = this;
			annotationUI.Initialize(mOpenAnnotationDialog.FileName);
			annotationUI.Show();
			annotationUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenIssueClick(object sender, EventArgs e)
	{
		if (mOpenIssueDialog.ShowDialog() == DialogResult.OK)
		{
			IssueUI issueUI = new IssueUI();
			issueUI.MdiParent = this;
			issueUI.Initialize(mOpenIssueDialog.FileName);
			issueUI.Show();
			issueUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenCapitalClick(object sender, EventArgs e)
	{
		if (mOpenEquityDialog.ShowDialog() == DialogResult.OK)
		{
			EquityUI equityUI = new EquityUI();
			equityUI.MdiParent = this;
			equityUI.Initialize(mOpenEquityDialog.FileName);
			equityUI.Show();
			equityUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenCapitalistClick(object sender, EventArgs e)
	{
		if (mOpenCapitalistDialog.ShowDialog() == DialogResult.OK)
		{
			CapitalistUI capitalistUI = new CapitalistUI();
			capitalistUI.MdiParent = this;
			capitalistUI.Initialize(mOpenCapitalistDialog.FileName);
			capitalistUI.Show();
			capitalistUI.WindowState = FormWindowState.Maximized;
		}
	}

	private void OnOpenStockholderClick(object sender, EventArgs e)
	{
		if (mOpenStockholderDialog.ShowDialog() == DialogResult.OK)
		{
			StockholderUI stockholderUI = new StockholderUI();
			stockholderUI.MdiParent = this;
			stockholderUI.Initialize(mOpenStockholderDialog.FileName);
			stockholderUI.Show();
			stockholderUI.WindowState = FormWindowState.Maximized;
		}
	}
}
