using SQLite.CodeFirst;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace 同花顺导入.Db
{
    /// <summary>
    /// 
    /// </summary>
    public class OrmContext:DbContext
    {
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            // 没有的话就创建数据库，已经有了就不创建了
            var sqliteConnectionInitializer = new SqliteCreateDatabaseIfNotExists<OrmContext>(modelBuilder);
            Database.SetInitializer(sqliteConnectionInitializer);
        }

        public OrmContext() : base("DatabaseContext")
        {

        }

        public DbSet<Models.D1BarFileModel> D1BarFileModels { get; set; }
    }
}
