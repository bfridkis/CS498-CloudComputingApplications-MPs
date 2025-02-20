import java.io.IOException;

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

public class TablePartE{

   public static void main(String[] args) throws IOException {

	// TODO      
	
	//Create table connection (See TablePartA.java for more detailed comments on these functions)
	Configuration config = HBaseConfiguration.create();
	
	try(Connection connection = ConnectionFactory.createConnection(config)) {
	
		//Get the powers table
		Table table = connection.getTable(TableName.valueOf("powers"));

		//Set up scanner
		Scan scan = new Scan();
		
		//Set up result scanner
		ResultScanner scanner = table.getScanner(scan);
		
		// DON' CHANGE THE 'System.out.println(xxx)' OUTPUT PART
		// OR YOU WON'T RECEIVE POINTS FROM THE GRADER
		for (Result result = scanner.next(); result != null; result = scanner.next())
			System.out.println(result);
	}
	catch (IOException e) {
		  System.err.println("Error processing CSV file or HBase: " + e.getMessage());
	  } 
   }
}

