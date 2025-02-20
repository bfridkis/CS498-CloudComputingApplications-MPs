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

public class TablePartG{

   public static void main(String[] args) throws IOException {

	// TODO      
	// DON' CHANGE THE 'System.out.println(xxx)' OUTPUT PART
	// OR YOU WON'T RECEIVE POINTS FROM THE GRADER      


	//Create table connection (See TablePartA.java for more detailed comments on these functions)
	Configuration config = HBaseConfiguration.create();
	  
	try (Connection connection = ConnectionFactory.createConnection(config);
		   Table table = connection.getTable(TableName.valueOf("powers"));
		   Table table1 = connection.getTable(TableName.valueOf("powers"))) {
			
			//Set up scanner for outer loop
			Scan scan = new Scan();
			ResultScanner scanner = table.getScanner(scan);
			
			int resultCount = 0;
			for (Result result = scanner.next(); result != null; result = scanner.next()) {
				//Set up scanner for inner loop
				Scan scan1 = new Scan();
				ResultScanner scanner1 = table1.getScanner(scan1);
				//Perform simulated "join" operation
				for (Result result1 = scanner1.next(); result1 != null; result1 = scanner1.next()) {
	
					// DON' CHANGE THE 'System.out.println(xxx)' OUTPUT PART
					// OR YOU WON'T RECEIVE POINTS FROM THE GRADER
					String name = Bytes.toString(result.getValue(Bytes.toBytes("professional"),Bytes.toBytes("name")));
					String power = Bytes.toString(result.getValue(Bytes.toBytes("personal"),Bytes.toBytes("power")));
					String color = Bytes.toString(result.getValue(Bytes.toBytes("custom"),Bytes.toBytes("color")));

					String name1 = Bytes.toString(result1.getValue(Bytes.toBytes("professional"),Bytes.toBytes("name")));
					String power1 = Bytes.toString(result1.getValue(Bytes.toBytes("personal"),Bytes.toBytes("power")));
					String color1 = Bytes.toString(result1.getValue(Bytes.toBytes("custom"),Bytes.toBytes("color")));
					//if(color == color1) System.out.println(name + ", " + power + ", " + name1 + ", " + power1 + ", "+color + ", " + color1);
					if (!name.equals(name1) && color.equals(color1)) {
						System.out.println(name + ", " + power + ", " + name1 + ", " + power1 + ", "+color);
						resultCount++;
					}
				}
			}
			//System.out.println("Rows Returned: " + resultCount);
	}
	catch (IOException e) {
		  System.err.println("Error processing HBase: " + e.getMessage());
	  }	

   }
}
