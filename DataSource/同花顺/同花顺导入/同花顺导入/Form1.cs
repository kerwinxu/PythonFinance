using Oci.Athena.DataSource.Hexin;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using 同花顺导入.Db;
using 同花顺导入.Models;

namespace 同花顺导入
{
    public partial class Form1 : Form
    {

        // todo 日线文件相比较同花顺安装目录，其他的文件
        // todo 数据库文件，日志文件，配置文件，等等

        private string sz_day_dir = "history\\sznse\\day";
        private string sh_day_dir = "history\\shase\\day";


        public Form1()
        {
            InitializeComponent();

            //OrmContext ormContext = new OrmContext();
            //var count = ormContext.D1BarFileModels.Count();
            //Debug.WriteLine($"现在共有日线行数:{count}");
        }

        /// <summary>
        /// 更新步骤的显示，注意这里需要在UI线程中操作，所以使用Invoke方法来更新UI控件的状态
        /// </summary>
        /// <param name="msg"></param>
        private void updateSetp(string msg)
        {
            this.Invoke(new Action(() => this.lblStep.Text = msg));
        }

        /// <summary>
        /// 选择文件夹
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSelectInstallDir_Click(object sender, EventArgs e)
        {
            if(this.folderBrowserDialog1.ShowDialog() == DialogResult.OK)
            {
                this.txtSource.Text = this.folderBrowserDialog1.SelectedPath;
            }
        }

        /// <summary>
        ///  设置总进度条的值，最大值，最小值等，注意这里需要在UI线程中操作，所以使用Invoke方法来更新UI控件的状态
        /// </summary>
        /// <param name="progress"></param>
        /// <param name="max"></param>
        private void updateProgress1(int progress, int max)
        {
            this.Invoke(new Action(() => { 
                this.progressBar1.Value = progress; 
                this.progressBar1.Maximum = max;
                this.progressBar1.Minimum = 0;
            }));
        }

        /// <summary>
        ///  设置详细进度条的值，最大值，最小值等，注意这里需要在UI线程中操作，所以使用Invoke方法来更新UI控件的状态
        /// </summary>
        /// <param name="progress"></param>
        /// <param name="max"></param>
        private void updateProgress2(int progress, int max)
        {
            this.Invoke(new Action(() => {
                this.progressBar2.Value = progress;
                this.progressBar2.Maximum = max;
                this.progressBar2.Minimum = 0;
            }));
        }

        /// <summary>
        /// 日线处理
        /// </summary>
        /// <param name="install_dir"></param>
        private void step_day(string install_dir)
        {
            // 这里先取得这个文件夹有多少个文件吧
            DirectoryInfo info = new DirectoryInfo(System.IO.Path.Combine(install_dir, sz_day_dir));
            DirectoryInfo info2 = new DirectoryInfo(System.IO.Path.Combine(install_dir, sh_day_dir));
            List<FileInfo> files = new List<FileInfo>();
            files.AddRange(info.GetFiles("*.day"));  // 这里是取得所有的日线文件
            files.AddRange(info2.GetFiles("*.day"));  // 这里是取得所有的日线文件
            OrmContext context = new OrmContext();    // 操作数据库的上下文对象，这里是每个步骤都创建一个新的上下文对象，实际情况可以根据需要来调整，比如说在整个导入过程中只创建一个上下文对象，等等
            DateTime start_time = DateTime.Now;
            for (int i = 0; i < files.Count; i++)
            {
                var file_path = files[i].FullName;
                var code = Path.GetFileNameWithoutExtension(file_path);
                //Thread.Sleep(100); // 这里模拟一下处理文件的时间，实际情况可以根据需要来调整
                // 这里实际的处理文件。
                D1BarFile file = new D1BarFile();
                using (var stream = File.OpenRead(file_path))
                {
                    var flag = D1BarFile.Read(ref file, stream);
                    if (flag) { 
                        // 这里看一下实际的内容
                        var recordList = file.RecordList;
                        // 这里可以根据实际情况来处理这些记录，比如说导入到数据库中，或者是写入到其他的文件中，等等
                        // 我这里是批量处理的，这里进行批量插入操作
                        var models = recordList.Select(x => new D1BarFileModel(code, x)).ToArray();
                        context.BulkInsert(models); // 这里是批量插入的方法，实际情况可以根据需要来调整，比如说使用普通的插入方法，等等
                        context.BulkSaveChanges();

                    }
                }
                updateProgress2(i + 1, files.Count); // 进度条
                updateSetp($"{i+1}/{files.Count}");  // 进度条的文本

            }
            

        }

        public delegate void StepDelegate(string install_dir);

        private void btnStart_Click(object sender, EventArgs e)
        {
            // 这里首先删除原先的
            FileInfo fileInfo = new FileInfo(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "sqlite.db"));
            File.Delete(fileInfo.FullName); 


            // 这里首先检查一下安装目录是否正确，是否存在日线文件夹，等等
            // 这里再线程中操作
            Task.Run(() => {
                string installDir = this.txtSource.Text.Trim();
                if (string.IsNullOrEmpty(installDir))
                {
                    MessageBox.Show("请先选择安装目录！");
                    return;
                }
                string dayDir = System.IO.Path.Combine(installDir, sz_day_dir);
                if (!System.IO.Directory.Exists(dayDir))
                {
                    MessageBox.Show("安装目录中没有找到日线文件夹，请检查安装目录是否正确！");
                    return;
                }
                // 这里先设置一下有多少步骤
                var _step_day = new StepDelegate(step_day);

                List<StepDelegate> steps = new List<StepDelegate>() { _step_day };
                for (global::System.Int32 i = 0; i < steps.Count; i++)
                {
                    steps[i](installDir);
                    updateProgress1(i+1, steps.Count);
                }


                // 这里可以继续检查其他的文件，数据库文件，日志文件，配置文件，等等
                // 如果检查通过了，就可以开始导入了，这里就不写具体的导入逻辑了，可以根据实际情况来实现
                // 导入过程中可以调用updateSetp方法来更新步骤的显示，调用updateProgress1和updateProgress2方法来更新进度条的显示
            });
        }
    }
}
