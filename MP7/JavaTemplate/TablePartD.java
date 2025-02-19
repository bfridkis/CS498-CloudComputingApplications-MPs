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

public class TablePartD{

   public static void main(String[] args) throws IOException {

	// TODO      
	// DON' CHANGE THE 'System.out.println(xxx)' OUTPUT PART
	// OR YOU WON'T RECEIVE POINTS FROM THE GRADER 
	
	//Create table connection (See TablePartA.java for more detailed comments on these functions)
	Configuration config = HBaseConfiguration.create();
	Connection connection = ConnectionFactory.createConnection(config);
	
	//Get the powers table
	Table table = connection.getTable(TableName.valueOf("powers"));
	
	//Get row 1 using Get and Result classes
	Get g = new Get(Bytes.toBytes("row1"));
	Result result = table.get(g);
	
	// Reading values from Result class object, all fields
    byte [] hero1 = result.getValue(Bytes.toBytes("personal"),Bytes.toBytes("hero"));
    byte [] power1 = result.getValue(Bytes.toBytes("personal"),Bytes.toBytes("power"));
    byte [] name1 = result.getValue(Bytes.toBytes("professional"),Bytes.toBytes("name"));
    byte [] xp1 = result.getValue(Bytes.toBytes("professional"),Bytes.toBytes("xp"));
    byte [] color1 = result.getValue(Bytes.toBytes("custom"),Bytes.toBytes("color"));
	
	String hero = Bytes.toString(hero1);
	String power = Bytes.toString(power1);
	String name = Bytes.toString(name1);
	String xp = Bytes.toString(xp1);
	String color = Bytes.toString(color1);
	System.out.println("hero: "+hero+", power: "+power+", name: "+name+", xp: "+xp+", color: "+color);

	//Get row 19 using Get and Result classes
	g = new Get(Bytes.toBytes("row19"));
	result = table.get(g);
	
	// Reading values from Result class object, hero and color
    byte [] hero19 = result.getValue(Bytes.toBytes("personal"),Bytes.toBytes("hero"));
    byte [] color19 = result.getValue(Bytes.toBytes("custom"),Bytes.toBytes("color"));

	hero = Bytes.toString(hero19);
	color = Bytes.toString(color19);
	System.out.println("hero: "+hero+", color: "+color);

	hero = Bytes.toString(hero1);
	name = Bytes.toString(name1);
	color = Bytes.toString(color1);
	System.out.println("hero: "+hero+", name: "+name+", color: "+color); 
   }
}

// References
// https://www.tutorialspoint.com/hbase/hbase_read_data.htm
// https://stackoverflow.com/questions/17939084/get-all-values-of-all-rows-in-hbase-using-java
