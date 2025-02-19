import java.io.IOException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.BufferedReader;

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

public class TablePartC{

   public static void main(String[] args) throws IOException {

	//TODO      
	
	//Create table connection (See TablePartA.java for more detailed comments on these functions)
	  Configuration config = HBaseConfiguration.create();
	  
	  try (Connection connection = ConnectionFactory.createConnection(config);
		   Table table = connection.getTable(TableName.valueOf("powers"));
           BufferedReader br = new BufferedReader(new FileReader("input.csv"))) {
				String line;
            while ((line = br.readLine()) != null) {
                String[] fields = line.split(",");

                // First field is the row key
                String rowKey = fields[0];
				
				//Build new row using fields[0] as row key
                Put put = new Put(Bytes.toBytes(rowKey));
				
				//Add the hero and power fields to the 'personal' column family
				put.addColumn(Bytes.toBytes("personal"), Bytes.toBytes("hero"), Bytes.toBytes(fields[1]));
				put.addColumn(Bytes.toBytes("personal"), Bytes.toBytes("power"), Bytes.toBytes(fields[2]));
				
				//Add the name and xp fields to the 'professional' column family
				put.addColumn(Bytes.toBytes("professional"), Bytes.toBytes("name"), Bytes.toBytes(fields[3]));
				put.addColumn(Bytes.toBytes("professional"), Bytes.toBytes("xp"), Bytes.toBytes(fields[4]));
				
				//Add the color field to the 'custom' column family
				put.addColumn(Bytes.toBytes("custom"), Bytes.toBytes("color"), Bytes.toBytes(fields[5]));
				
                table.put(put);
            }
	  }
	  catch (IOException e) {
		  System.err.println("Error processing CSV file or HBase: " + e.getMessage());
	  }
   }
}

// References
// https://www.google.com/search?q=load+.csv+file+into+hbase+table+with+java+example&rlz=1C1CHBF_enUS1071US1071&oq=load+.csv+file+into+hbase+table+with+java+example&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRiPAtIBCDk1NTRqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8