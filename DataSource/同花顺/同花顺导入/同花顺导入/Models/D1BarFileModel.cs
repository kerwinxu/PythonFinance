using Oci.Athena.DataSource.Hexin;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace 同花顺导入.Models
{
    
    public class D1BarFileModel
    {
        /// <summary>
        /// id
        /// </summary>
        [Key]
        
        public int Id { get; set; }


        /// <summary>
        /// 股票代码
        /// </summary>
        [Index("IxCode",1)]
        public string Code { get; set; }

        /// <summary>
        /// 日期
        /// </summary>
        [Index("IxCode", 2)]
        public DateTime Date { get; set; }

        public double Open { get; set; }

        public double High { get; set; }

        public double Low { get; set; }

        public double Close { get; set; }   

        public double Amount { get; set; }  

        public double Volume { get; set; }

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="d1BarFile"></param>
        public D1BarFileModel(String code, D1BarRecord d1BarRecord)
        {
            this.Id = 0;
            this.Code = code;
            this.Date = d1BarRecord.Date;
            this.Open = d1BarRecord.Open;
            this.High = d1BarRecord.High;
            this.Low = d1BarRecord.Low;
            this.Close = d1BarRecord.Close;
            this.Amount = d1BarRecord.Amount;
            this.Volume = d1BarRecord.Volume;

        }
    }
}
