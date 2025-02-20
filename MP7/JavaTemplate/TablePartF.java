import java.io.IOException;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
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

public class TablePartF{

   public static void main(String[] args) throws IOException {

	// TODO      
	// DON' CHANGE THE 'System.out.println(xxx)' OUTPUT PART
	// OR YOU WON'T RECEIVE POINTS FROM THE GRADER
	   
	//1. update the data in a particular cell using the put() method
	
	//Create table connection (See TablePartA.java for more detailed comments on these functions)
	  Configuration config = HBaseConfiguration.create();
	  
	  try (Connection connection = ConnectionFactory.createConnection(config);
		   Table table = connection.getTable(TableName.valueOf("powers"))) {
			
			//Update max versions for custom column family to 2
			// NOT NEEDED AS WE ACCOMPLISHED THIS IN PART A WHEN ESTABLISHING THE TABLE ITSELF, SPECIFICALLY FOR THE CUSTOM COLUMN FAMILY
			
			//Set up a put for key "row7"
			Put p = new Put(Bytes.toBytes("row7"));
			
			//Update the color value 
			p.addColumn(Bytes.toBytes("custom"), Bytes.toBytes("color"), Bytes.toBytes("purple"));
			//p.setAttribute("color", Bytes.toBytes("pink"));
			table.put(p);
			
			//2. Reading values from Result class object to retrieve all versions of all columns, with the most recent version coming first
			
			//Get row 7 using Get and Result classes
			Get g = new Get(Bytes.toBytes("row7"));
			Result result = table.get(g);
			
			//Only gets latest version of each cell...
			for (Cell cell : result.listCells()) {
				byte[] family = Bytes.copy(cell.getFamilyArray(),cell.getFamilyOffset(),cell.getFamilyLength());
				byte[] qualifier = Bytes.copy(cell.getQualifierArray(),cell.getQualifierOffset(),cell.getQualifierLength());
				byte[] value = Bytes.copy(cell.getValueArray(),cell.getValueOffset(),cell.getValueLength());
				long timestamp = cell.getTimestamp();

				System.out.println(
					"row: " + "row7" +
					", family: " + Bytes.toString(family) +
					", qualifier: " + Bytes.toString(qualifier) +
					", value: " + Bytes.toString(value) +
					", timestamp: " + timestamp
				);
			}
			
			//Thought I needed to do something like this, but didn't realize there is no NavigableMap class available for the assignment...
			/* NavigableMap<byte[], NavigableMap<byte[], NavigableMap<Long, byte[]>>> resultMap = result.getMap();
			byte[] family_;
			byte[] qualifier;
			byte[] value_;
			long timestamp_;
			if (resultMap != null && !resultMap.isEmpty()) {
                resultMap.forEach((family, columnMap) -> {
                    //System.out.println("Family: " + Bytes.toString(family));
					family_ = family;
                    columnMap.forEach((column, versionMap) -> {
                        //System.out.println("\tColumn: " + Bytes.toString(column));
						qualifier = column;
                        versionMap.forEach((timestamp, value) -> {
                            //System.out.println("\t\tTimestamp: " + timestamp + ", Value: " + Bytes.toString(value));
							value_ = value;
							timestamp_ = timestamp;
							System.out.println(
								"row: " + "row7" +
								", family: " + Bytes.toString(family) +
								", qualifier: " + Bytes.toString(column) +
								", value: " + Bytes.toString(value) +
								", timestamp: " + timestamp
							);
                        });
                    });
                });
            } else {
                System.out.println("No data found for the given row key.");
            } */
	  }
	  catch (IOException e) {
		  System.err.println("Error processing CSV file or HBase: " + e.getMessage());
	  }	

   }
}

// References
// https://stackoverflow.com/questions/34909897/hbase-extracting-value-and-timestamp-from-a-cell
// https://www.tutorialspoint.com/hbase/hbase_read_data.htm#:~:text=You%20can%20retrieve%20data%20from,Get%20class%20object%20as%20parameter.
// https://stackoverflow.com/questions/34909897/hbase-extracting-value-and-timestamp-from-a-cell
// https://hbase.apache.org/book.html#schema.versions.max
// https://stackoverflow.com/questions/64596319/trying-to-understand-updates-in-hbase
