namespace 同花顺导入
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.txtSource = new System.Windows.Forms.TextBox();
            this.btnStart = new System.Windows.Forms.Button();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.lblStep = new System.Windows.Forms.Label();
            this.btnSelectInstallDir = new System.Windows.Forms.Button();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.progressBar2 = new System.Windows.Forms.ProgressBar();
            this.SuspendLayout();
            // 
            // txtSource
            // 
            this.txtSource.Location = new System.Drawing.Point(83, 19);
            this.txtSource.Name = "txtSource";
            this.txtSource.Size = new System.Drawing.Size(599, 21);
            this.txtSource.TabIndex = 1;
            this.txtSource.Text = "D:\\同花顺软件\\同花顺";
            // 
            // btnStart
            // 
            this.btnStart.Location = new System.Drawing.Point(156, 102);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(75, 23);
            this.btnStart.TabIndex = 2;
            this.btnStart.Text = "开始";
            this.btnStart.UseVisualStyleBackColor = true;
            this.btnStart.Click += new System.EventHandler(this.btnStart_Click);
            // 
            // progressBar1
            // 
            this.progressBar1.Location = new System.Drawing.Point(83, 46);
            this.progressBar1.Name = "progressBar1";
            this.progressBar1.Size = new System.Drawing.Size(599, 23);
            this.progressBar1.TabIndex = 3;
            // 
            // lblStep
            // 
            this.lblStep.AutoSize = true;
            this.lblStep.BackColor = System.Drawing.Color.Transparent;
            this.lblStep.Location = new System.Drawing.Point(413, 80);
            this.lblStep.Name = "lblStep";
            this.lblStep.Size = new System.Drawing.Size(53, 12);
            this.lblStep.TabIndex = 4;
            this.lblStep.Text = "源文件夹";
            // 
            // btnSelectInstallDir
            // 
            this.btnSelectInstallDir.Location = new System.Drawing.Point(2, 17);
            this.btnSelectInstallDir.Name = "btnSelectInstallDir";
            this.btnSelectInstallDir.Size = new System.Drawing.Size(75, 23);
            this.btnSelectInstallDir.TabIndex = 5;
            this.btnSelectInstallDir.Text = "安装文件夹";
            this.btnSelectInstallDir.UseVisualStyleBackColor = true;
            this.btnSelectInstallDir.Click += new System.EventHandler(this.btnSelectInstallDir_Click);
            // 
            // progressBar2
            // 
            this.progressBar2.Location = new System.Drawing.Point(83, 75);
            this.progressBar2.Name = "progressBar2";
            this.progressBar2.Size = new System.Drawing.Size(599, 23);
            this.progressBar2.TabIndex = 6;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(736, 148);
            this.Controls.Add(this.btnSelectInstallDir);
            this.Controls.Add(this.lblStep);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.btnStart);
            this.Controls.Add(this.txtSource);
            this.Controls.Add(this.progressBar2);
            this.Name = "Form1";
            this.Text = "同花顺导入";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.TextBox txtSource;
        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Label lblStep;
        private System.Windows.Forms.Button btnSelectInstallDir;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.ProgressBar progressBar2;
    }
}

