import java.io.IOException;
import java.util.List;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;

import org.apache.hadoop.hbase.TableName;

import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.client.TableDescriptor;

import org.apache.hadoop.hbase.util.Bytes;

public class TablePartB{

   public static void main(String[] args) throws IOException {

      //TODO    
	  
	  //Create table connection (See TablePartA.java for more detailed comments on these functions)
	  Configuration config = HBaseConfiguration.create();
	  Connection connection = ConnectionFactory.createConnection(config);
	  
	  //Create an admin instance
	  Admin admin = connection.getAdmin();
	  
	  // List all tables on the cluster
      List<TableDescriptor> tableDescriptors = admin.listTableDescriptors();
	  
      for(TableDescriptor tableDescriptor : tableDescriptors){
            System.out.println(tableDescriptor.getTableName());
      }
   }
}

// References
// https://www.google.com/search?q=example+use+of+the+org.apache.hadoop.hbase.client.Admin+class+listing+tables&sca_esv=6fe806cc0ee527f3&rlz=1C1CHBF_enUS1071US1071&ei=bva0Z9v-IKvhp84PrdvtgA8&ved=0ahUKEwjb7YCqkM6LAxWr8MkDHa1tG_AQ4dUDCBA&uact=5&oq=example+use+of+the+org.apache.hadoop.hbase.client.Admin+class+listing+tables&gs_lp=Egxnd3Mtd2l6LXNlcnAiTGV4YW1wbGUgdXNlIG9mIHRoZSBvcmcuYXBhY2hlLmhhZG9vcC5oYmFzZS5jbGllbnQuQWRtaW4gY2xhc3MgbGlzdGluZyB0YWJsZXNI4BJQqAVYqRJwAXgAkAEAmAHMAaAB3AuqAQU3LjYuMbgBA8gBAPgBAZgCAKACAJgDAIgGAZIHAKAHrgw&sclient=gws-wiz-serp
// https://hbase.apache.org/apidocs/org/apache/hadoop/hbase/client/package-summary.html
// https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/client/Admin.html#listTableDescriptors--
// https://hbase.apache.org/2.3/apidocs/org/apache/hadoop/hbase/client/TableDescriptor.html
