import java.io.IOException;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;

import org.apache.hadoop.hbase.TableName;

import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptorBuilder;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.client.TableDescriptor;
import org.apache.hadoop.hbase.client.TableDescriptorBuilder;

import org.apache.hadoop.hbase.util.Bytes;

public class TablePartA{

   public static void main(String[] args) throws IOException {

	//TODO
	
	// You need a configuration object to tell the client where to connect.
    // When you create a HBaseConfiguration, it reads in whatever you've set
    // into your hbase-site.xml and in hbase-default.xml, as long as these can
    // be found on the CLASSPATH
	Configuration config = HBaseConfiguration.create();
	
	// Next you need a Connection to the cluster. Create one. When done with it,
    // close it. A try/finally is a good way to ensure it gets closed or use
    // the jdk7 idiom, try-with-resources: see
    // https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html
    //
    // Connections are heavyweight.  Create one once and keep it around. From a Connection
    // you get a Table instance to access Tables, an Admin instance to administer the cluster,
    // and RegionLocator to find where regions are out on the cluster. As opposed to Connections,
    // Table, Admin and RegionLocator instances are lightweight; create as you need them and then
    // close when done.
	Connection connection = ConnectionFactory.createConnection(config);
	
	//Create an admin instance
	Admin admin = connection.getAdmin();
	
	// Create a new "powers" table
	TableName tableName = TableName.valueOf("powers");
	
	//HTableDescriptor is a class that belongs to the org.apache.hadoop.hbase class. This class is like a container of table names and column families.
	//creating table descriptor for powers table
	//HTableDescriptor table = new HTableDescriptor(tableName);    //Deprecated
	//TableDescriptor table = new TableDescriptor(tableName);	   //Doesn't work because TableDescriptor is an abstract class

	//creating column family descriptors for powers table
	//HColumnDescriptor personal = new HColumnDescriptor(toBytes("personal"));
	//HColumnDescriptor professional = new HColumnDescriptor(toBytes("professional"));
	//HColumnDescriptor custom = new HColumnDescriptor(toBytes("custom"));
	//custom.setMaxVersions(2);

	//adding coloumn families to powers table
	//table.addFamily(new HColumnDescriptor("personal"));
	//table.addFamily(new HColumnDescriptor("professional"));
	//table.addFamily(new HColumnDescriptor("custom"));
	//table.addFamily(custom);
	
	//admin.createTable(table);
	
	TableDescriptorBuilder tBuilder = TableDescriptorBuilder.newBuilder(tableName);
	//ColumnFamilyDescriptor PERSONAL = ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("personal")).build();
	TableDescriptor tDesc = tBuilder.setColumnFamily(ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("personal")).build()).build();
	//ColumnFamilyDescriptor PROFESSIONAL = ColumnFamilyDescriptorBuilder.newBuilder("professional").build();
	tDesc = tBuilder.setColumnFamily(ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("professional")).build()).build();
	//ColumnFamilyDescriptor CUSTOM = ColumnFamilyDescriptorBuilder.newBuilder("custom").setMaxVersions(2).build();
	tDesc = tBuilder.setColumnFamily(ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("custom")).setMaxVersions(2).build()).build();
	admin.createTable(tDesc);
	
	System.out.println("'Powers' Table created ");
	
	// Create a new "food" table -- NOTE THIS USES A DEPRECATED METHOD, BUT KEPT JUST TO SHOW ANYWAY. METHOD ABOVE FOR CREATING POWERS TABLE IS CURRENT METHOD (i.e. is not deprecated)
	tableName = TableName.valueOf("food");
	HTableDescriptor table = new HTableDescriptor(tableName);
	//TableDescriptor table = new TableDescriptor(tableName);		//Doesn't work because TableDescriptor is an abstract class

	//creating column family descriptors for powers table
	//HColumnDescriptor nutrition = new HColumnDescriptor(toBytes("nutrition"));
	//HColumnDescriptor taste = new HColumnDescriptor(toBytes("taste"));

	//adding coloumn families to food table
	table.addFamily(new HColumnDescriptor("nutrition"));
	table.addFamily(new HColumnDescriptor("taste"));
	
	admin.createTable(table);
	System.out.println("'Food' Table created ");
	
	// Next you need a Connection to the cluster. Create one. When done with it,
    // close it. A try/finally is a good way to ensure it gets closed or use
    // the jdk7 idiom, try-with-resources: see
    // https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html
    //
    // Connections are heavyweight.  Create one once and keep it around. From a Connection
    // you get a Table instance to access Tables, an Admin instance to administer the cluster,
    // and RegionLocator to find where regions are out on the cluster. As opposed to Connections,
    // Table, Admin and RegionLocator instances are lightweight; create as you need them and then
    // close when done.
	//Connection connection = ConnectionFactory.createConnection(config);
	
	
   }
}

// References
// https://hbase.apache.org/apidocs/org/apache/hadoop/hbase/client/package-summary.html
// https://www.tutorialspoint.com/hbase/hbase_create_table.htm
// https://www.google.com/search?q=example+use+of+the+org.apache.hadoop.hbase.client.Admin+class&rlz=1C1CHBF_enUS1071US1071&oq=example+use+of+the+org.apache.hadoop.hbase.client.Admin+class&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRigATIHCAIQIRirAjIHCAMQIRiPAtIBCDI2OTFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
// https://stackoverflow.com/questions/74088595/how-to-create-a-table-in-hbase-using-java-api
// https://www.google.com/search?q=example+of+using+columnfamilydescriptorbuilder&sca_esv=7833c6f0638101e1&rlz=1C1CHBF_enUS1071US1071&ei=wXa2Z87PEp7ep84Pvo3C0Q4&ved=0ahUKEwiOtLzs_tCLAxUe78kDHb6GMOoQ4dUDCBA&uact=5&oq=example+of+using+columnfamilydescriptorbuilder&gs_lp=Egxnd3Mtd2l6LXNlcnAiLmV4YW1wbGUgb2YgdXNpbmcgY29sdW1uZmFtaWx5ZGVzY3JpcHRvcmJ1aWxkZXIyBxAhGKABGAoyBxAhGKABGAoyBxAhGKABGAoyBRAhGJ8FSOUEUL8DWL8DcAF4AJABAJgBbqABbqoBAzAuMbgBA8gBAPgBAZgCAaACcpgDAIgGAZIHAzAuMaAHpQY&sclient=gws-wiz-serp