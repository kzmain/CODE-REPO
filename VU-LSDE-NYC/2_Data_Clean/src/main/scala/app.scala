import java.io.{File, FileWriter, PrintWriter}
import java.text.SimpleDateFormat
import java.util.Date
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
//----------------------------------------------------------------------------------------------------------------------
//       2019 LSDE GROUP 11 KAI ZHANG/YI ZHEN ZHAO/YU WANG
//       Last Update: 05-10-2019 13:16
//       Version: 1.1
//
//       # Description: This Spark/Scala script is target to clean data
//       * Included:
//         * process_yellow_taxi_before_2017() : 
//             Yellow taxi's pick up location/drop off location data before 2016.07 is recorded by longitude/latitude
//             -> Basic Procedure: Reset Heading
//             -> Filter lon/lat (Write out wrong data for backup) 
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Filter length > 200m (Write out wrong data for backup) 
//             -> Write out cleaned result partitioned by date
//             -> Write out logs
//         * process_yellow_taxi_after_2017()
//             Yellow taxi's pick up location/drop off location data after 2016.07 is recorded by taxi zones
//             -> Basic Procedure: Reset Heading
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Filter length > 200m (Write out wrong data for backup) 
//             -> Write out cleaned result partitioned by date
//             -> Write out logs
//         * process_green_taxi_before_2016_07()
//             Green taxi's pick up location/drop off location data before 2016.07 is recorded by longitude/latitude
//             -> Basic Procedure: Reset Heading
//             -> Filter lon/lat (Write out wrong data for backup) 
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Filter length > 200m (Write out wrong data for backup) 
//             -> Write out cleaned result partitioned by date
//             -> Write out logs
//         * process_green_taxi_after_2016_07()
//             Green taxi's pick up location/drop off location data after 2016.07 is recorded by taxi zones
//             -> Basic Procedure: Reset Heading
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Filter length > 200m (Write out wrong data for backup) 
//             -> Write out cleaned result partitioned by date
//             -> Write out logs
//         * process_fhv_before_2017()
//             Notice: FHV's data has pick up time but does not have drop off time, so did not check duration.
//             FHV taxi's data before 2017 only has pick up taxi zone and pick up date time so we do not check time (duration)
//             -> Basic Procedure: Reset Heading
//             -> Check null/not null pick id number
//             -> Write out result
//             -> Write out logs
//         * process_fhv_after_2017()
//             FHV taxi's data after 2017 has pick up/drop off taxi zone
//             -> Basic Procedure: Reset Heading
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Check null/not null pick id number
//             -> Write out result
//             -> Write out logs
//         * process_hfhv()
//             -> Basic Procedure: Reset Heading
//             -> Filter time >= 45s (Write out wrong data for backup) 
//             -> Check null/not null pick id number
//             -> Write out result
//             -> Write out logs
//       # Data Clean Little Explanation:
//          We have four types of taxi data, and they have different table headings, 
//          futhermore we even have different headings in one taxi type's data, so we made a table to illustrate how 
//          table headings changes between raw data and cleaned data. It's at 'LSDE-NYC/Documents/table_table_headings_of_taxi_data.xlsx'
//
//          About data structure align, we will use another scripts to convert all longitude/latitude to taxi zone but it is not done in
//          this part.
//       # Data Log:
//          * /Data/NYC_Trip_Data/yellow_result_2009_01_2016_12.csv:
//              year,month,raw_data_count,location_error_count,time_error_count,distance_errror_count,cleaned_data_count
//          * /Data/NYC_Trip_Data/yellow_error_2009_01_2016_12.txt:
//             Exception: year month yellow taxi data not found.
//          * /Data/NYC_Trip_Data/yellow_result_2017_01_2019_12.csv:
//              year,month,raw_data_count,time_error_count,distance_errror_count,cleaned_data_count
//          * /Data/NYC_Trip_Data/yellow_error_2017_01_2019_12.txt:
//             Exception: year month yellow taxi data not found.
//          * /Data/NYC_Trip_Data/green_result_2013_08_2016_06.csv:
//              year,month,raw_data_count,location_error_count,time_error_count,distance_errror_count,cleaned_data_count
//          * /Data/NYC_Trip_Data/green_error_2013_08_2016_06.txt:
//             Exception: year month green taxi data not found.
//          * /Data/NYC_Trip_Data/green_result_2016_07_2019_12.csv:
//              year,month,raw_data_count,time_error_count,distance_errror_count,cleaned_data_count
//          * /Data/NYC_Trip_Data/green_error_2016_07_2019_12.txt:
//             Exception: year month green taxi data not found.
//          * /Data/NYC_Trip_Data/fhv_result_2015_01_2017_01.csv:
//              year,month,count_is_null,count_is_not_null,cleaned_data_count
//          * /Data/NYC_Trip_Data/fhv_errors_2015_01_2017_01.txt
//              Exception: year month fhv taxi data not found.
//          * /Data/NYC_Trip_Data/fhv_result_2017_01_2019_12.csv
//              year,month,raw_data_count,count_is_null,count_is_not_null,cleaned_data_count
//          * /Data/NYC_Trip_Data/fhv_errors_2017_01_2019_12.txt
//              Exception: year month fhv taxi data not found.
//          * /Data/NYC_Trip_Data/fhvhv_result_2019.csv
//              year,month,raw_data_count,count_is_null,count_is_not_null,cleaned_data_count
//          * /Data/NYC_Trip_Data/fhvhv_errors_2019.txt
//              Exception: year month fhvhv taxi data not found.
//       # Potential Problem:
//           * The way we clean location is not that accurate, because we used four bounds to filter out trips not in NYC. 
//           we did not check it if it is excatly in NYC Polygon. It is estimated that 0.01% in cleaned data is start/finished out of NYC.
//           * Yellow's data after 2016.6 p_id/d_id may have null
//           * Green's data after 2016.6 p_id/d_id may have null
//           * All FHV/hvfhv p_id/d_id may have null
//----------------------------------------------------------------------------------------------------------------------
object app{
  val spark: SparkSession = SparkSession
    .builder
    .appName("app").master("local[*]")
    .getOrCreate()
  import spark.implicits._

  // Local Mode
  val data_dir = "../Data/NYC_Trip_Data"
  val java_data_dir = "../Data/NYC_Trip_Data"

  // // Databricks Mode
  // val data_dir = "/mnt/group11/Data/NYC_Trip_Data"
  // val java_data_dir = "/dbfs/mnt/group11/Data/NYC_Trip_Data"

  // Bounds to filter trips out of NYC
  val w_lon: Double = -74.2463  //左 left bound
  val e_lon: Double = -73.7141  //右 right bound
  val n_lat: Double = 40.9166   //上 up bound
  val s_lat: Double = 40.4767   //下 down bound

  def process_yellow_taxi_before_2017(): Unit ={
    val file_statistic      = java_data_dir + "/yellow_result_2009_01_2016_12.csv"
    val file_error          = java_data_dir + "/yellow_result_2009_01_2016_12.txt"

    val path_loc_error      = data_dir + "/yellow_tripdata/error_location_"
    val path_time_error     = data_dir + "/yellow_tripdata/error_time_"
    val path_distance_error = data_dir + "/yellow_tripdata/error_distance_"
    val path_result         = data_dir + "/yellow_tripdata/result_"
    val path_raw            = data_dir + "/yellow_tripdata/yellow_tripdata_"
    // Create yellow taxi static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)
    print_Writer.write("Year,Month,Total,Location,Duration,Distance,Result\n")
    print_Writer.close()

    val s_year = 2009
    val e_year = 2017
    val s_month = 1
    val e_month = 12

    // Loop by year
    for(year <- s_year to e_year){
      for(int_month <- s_month to e_month){
        var month = ""
        if(int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try
        {
          val file_parquet =  year + "_" + month  + ".parquet"
          //Read in a month's yellow taxi data align table headings and set id
          var raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(path_raw + year + "-" + month + ".csv")
            .withColumn("id", monotonically_increasing_id())
          //2009's heading change to standard table heading
          if(raw_data.columns.contains("vendor_name")){
            raw_data = raw_data.select(
              $"id",
              $"Trip_Pickup_DateTime".as("p_datetime"),
              $"Trip_Dropoff_DateTime".as("d_datetime"),
              $"Rate_Code".as("rate_code_id"),
              $"Start_Lon".as("p_lon"),
              $"Start_Lat".as("p_lat"),
              $"End_Lon".as("d_lon"),
              $"End_Lat".as("d_lat"),
              $"Trip_Distance".as("trip_distance"),
              $"Fare_Amt".as("fare_amount"),
              $"mta_tax".as("mta_tax"),
              $"Tolls_Amt".as("tolls_amount"),
              $"surcharge"
            )
          }
          //2010-2014's heading change to standard table heading
          else if(raw_data.columns.contains("pickup_datetime")){
            raw_data = raw_data.select(
              $"id",
              $"pickup_datetime".as("p_datetime"),
              $"dropoff_datetime".as("d_datetime"),
              $"rate_code".as("rate_code_id"),
              $"pickup_longitude".as("p_lon"),
              $"pickup_latitude".as("p_lat"),
              $"dropoff_longitude".as("d_lon"),
              $"dropoff_latitude".as("d_lat"),
              $"trip_distance".as("trip_distance"),
              $"fare_amount".as("fare_amount"),
              $"mta_tax".as("mta_tax"),
              $"tolls_amount".as("tolls_amount"),
              $"surcharge"
            )
          }
          //2014's heading change to standard table heading
          else if(raw_data.columns.contains(" pickup_datetime")){
            raw_data = raw_data.select(
              $"id",
              $" pickup_datetime".as("p_datetime"),
              $" dropoff_datetime".as("d_datetime"),
              $" rate_code".as("rate_code_id"),
              $" pickup_longitude".as("p_lon"),
              $" pickup_latitude".as("p_lat"),
              $" dropoff_longitude".as("d_lon"),
              $" dropoff_latitude".as("d_lat"),
              $" trip_distance".as("trip_distance"),
              $" fare_amount".as("fare_amount"),
              $" mta_tax".as("mta_tax"),
              $" tolls_amount".as("tolls_amount"),
              $" surcharge".as("surcharge")
            )
          }
          //2015-2016's heading change to standard table heading
          else if(raw_data.columns.contains("VendorID")){
            raw_data = raw_data.select(
              $"id",
              $"tpep_pickup_datetime".as("p_datetime"),
              $"tpep_dropoff_datetime".as("d_datetime"),
              $"RatecodeID".as("rate_code_id"),
              $"pickup_longitude".as("p_lon"),
              $"pickup_latitude".as("p_lat"),
              $"dropoff_longitude".as("d_lon"),
              $"dropoff_latitude".as("d_lat"),
              $"trip_distance".as("trip_distance"),
              $"fare_amount".as("fare_amount"),
              $"mta_tax".as("mta_tax"),
              $"tolls_amount".as("tolls_amount"),
              $"improvement_surcharge".as("surcharge")
            )
          }
          //----------------------------------------------------------------------------------------------------------------------
          // Filter by longitude and latitude
          val loc_error = raw_data.filter(
            $"p_lon" > e_lon or $"p_lon" < w_lon or
              $"d_lon" > e_lon or $"d_lon" < w_lon or
              $"p_lat" > n_lat or $"p_lat" < s_lat or
              $"d_lat" > n_lat or $"d_lat" < s_lat or
              $"p_lon".isNull or $"d_lon".isNull or
              $"p_lat".isNull or $"d_lat".isNull
          )
          var result = raw_data.filter(
            $"p_lon" <= e_lon and $"p_lon" >= w_lon and
              $"d_lon" <= e_lon and $"d_lon" >= w_lon and
              $"p_lat" <= n_lat and $"p_lat" >= s_lat and
              $"d_lat" <= n_lat and $"d_lat" >= s_lat
          )

          loc_error.write.mode("overwrite").parquet( path_loc_error + file_parquet)

          //----------------------------------------------------------------------------------------------------------------------
          // Filter by duration
          val yellow_taxi_time =  result
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")

          val time_error = yellow_taxi_time.filter($"duration" < 45)
          time_error.write.mode("overwrite").parquet( path_time_error + file_parquet)
          result = yellow_taxi_time.filter($"duration" >= 45)
          //----------------------------------------------------------------------------------------------------------------------
          // Filter by distance
          val distance_error = result.filter($"trip_distance" <= 0.2)
          distance_error.write.mode("overwrite").parquet(path_distance_error + file_parquet)
          result = result.filter($"trip_distance" > 0.2)
          //----------------------------------------------------------------------------------------------------------------------
          // write result
          result.withColumn("total_amount", $"fare_amount" + $"tolls_amount")
            .select(
              $"id",
              $"p_date",
              $"p_time",
              $"p_hour",
              $"duration",
              $"p_lon",
              $"p_lat",
              $"d_lon",
              $"d_lat",
              $"trip_distance",
              $"tolls_amount",
              $"total_amount",
              $"rate_code_id",
              $"surcharge"
            )
            .write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)
          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + ","  +
            raw_data.count() + "," +
            loc_error.count() + "," +
            time_error.count() + "," +
            distance_error.count() + "," +
            result.count() + "\n")
          fw.close()
        }
        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " yellow taxi data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()


            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " yellow taxi data not found.\n")
              fw.close()
            }else{
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " yellow taxi data not found.\n")
              fw.close()
            }
        }
      }
    }
  }

  def process_yellow_taxi_after_2017(): Unit ={
    val file_statistic      = java_data_dir + "/yellow_result_2017_01_2019_12.csv"
    val file_error          = java_data_dir + "/yellow_result_2017_01_2019_12.txt"

    val path_time_error     = data_dir + "/yellow_tripdata/error_time_"
    val path_distance_error = data_dir + "/yellow_tripdata/error_distance_"
    val path_result         = data_dir + "/yellow_tripdata/result_"
    val path_raw            = data_dir + "/yellow_tripdata/yellow_tripdata_"
    // Create yellow taxi static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)
    print_Writer.write("Year,Month,Total,Duration,Distance,Result\n")
    print_Writer.close()

    val s_year = 2017
    val e_year = 2019
    val s_month = 1
    val e_month = 12
    // Loop by year
    for(year <- s_year to e_year) {
      for (int_month <- s_month to e_month) {
        var month = ""
        if (int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try {
          val file_parquet = year + "_" + month + ".parquet"
          //Read in a month's yellow taxi data align table headings and set id
          var raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(path_raw + year + "-" + month + ".csv")
            .withColumn("id", monotonically_increasing_id())
          //2017-2019's heading change to standard table heading
          if (raw_data.columns.contains("VendorID")) {
            raw_data = raw_data.select(
              $"id",
              $"tpep_pickup_datetime".as("p_datetime"),
              $"tpep_dropoff_datetime".as("d_datetime"),
              $"RatecodeID".as("rate_code_id"),
              $"PULocationID".as("p_id"),
              $"DOLocationID".as("d_id"),
              $"trip_distance".as("trip_distance"),
              $"fare_amount".as("fare_amount"),
              $"mta_tax".as("mta_tax"),
              $"tolls_amount".as("tolls_amount"),
              $"improvement_surcharge".as("surcharge")
            )
          }
          //----------------------------------------------------------------------------------------------------------------------
          // Filter by duration
          val yellow_taxi_time = raw_data
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")
          val time_error = yellow_taxi_time.filter($"duration" < 45)
          time_error.write.mode("overwrite").parquet(path_time_error + file_parquet)
          var result = yellow_taxi_time.filter($"duration" >= 45)
          //----------------------------------------------------------------------------------------------------------------------
          // Filter by distance
          val distance_error = result.filter($"trip_distance" <= 0.2)
          distance_error.write.mode("overwrite").parquet(path_distance_error + file_parquet)
          result = result.filter($"trip_distance" > 0.2)
          //----------------------------------------------------------------------------------------------------------------------
          // write result
          result.withColumn("total_amount", $"fare_amount" + $"tolls_amount")
            .select(
              $"id",
              $"p_date",
              $"p_time",
              $"p_hour",
              $"duration",
              $"p_id",
              $"d_id",
              $"trip_distance",
              $"tolls_amount",
              $"total_amount",
              $"rate_code_id",
              $"surcharge"
            )
            .write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)
          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            raw_data.count() + "," +
            time_error.count() + "," +
            distance_error.count() + "," +
            result.count() + "\n")
          fw.close()
        }
        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " yellow taxi data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()


            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " yellow taxi data not found.\n")
              fw.close()
            } else {
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " yellow taxi data not found.\n")
              fw.close()
            }
        }
      }
    }
  }

  def process_green_taxi_before_2016_07(): Unit ={
    val file_statistic      = java_data_dir + "/green_result_2013_08_2016_06.csv"
    val file_error          = java_data_dir + "/green_errors_2013_08_2016_06.txt"

    val path_loc_error      = data_dir + "/green_tripdata/error_location_"
    val path_time_error     = data_dir + "/green_tripdata/error_time_"
    val path_distance_error = data_dir + "/green_tripdata/error_distance_"
    val path_result         = data_dir + "/green_tripdata/result_"
    val path_raw            = data_dir + "/green_tripdata/green_tripdata_"
    // Create green taxi static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)
    print_Writer.write("Year,Month,Total,Location,Duration,Distance,Result\n")
    print_Writer.close()

    val s_year = 2013
    val e_year = 2019
    val s_month = 1
    val e_month = 12
    // Loop by year
    for(year <- s_year to e_year){
      for(int_month <- s_month to e_month){
        var month = ""
        if(int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try
        {
          val file_parquet =  year + "_" + month  + ".parquet"
          //Read in a month's green taxi data align table headings and set id
          val raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(path_raw + year + "-" + month + ".csv")
            .withColumn("id", monotonically_increasing_id())
            .select(
              $"id",
              $"lpep_pickup_datetime".as("p_datetime"),
              $"Lpep_dropoff_datetime".as("d_datetime"),
              $"RateCodeID".as("rate_code_id"),
              $"Pickup_longitude".as("p_lon"),
              $"Pickup_latitude".as("p_lat"),
              $"Dropoff_longitude".as("d_lon"),
              $"Dropoff_latitude".as("d_lat"),
              $"Trip_distance".as("trip_distance"),
              $"Fare_amount".as("fare_amount"),
              $"MTA_tax".as("mta_tax"),
              $"Tolls_amount".as("tolls_amount"),
              $"Trip_type ".as("trip_type")
            )
//----------------------------------------------------------------------------------------------------------------------
          // Filter by longitude and latitude
          var loc_error = raw_data.filter(
            $"p_lon" > e_lon or $"p_lon" < w_lon or
              $"d_lon" > e_lon or $"d_lon" < w_lon or
              $"p_lat" > n_lat or $"p_lat" < s_lat or
              $"d_lat" > n_lat or $"d_lat" < s_lat or
              $"p_lon".isNull  or $"d_lon".isNull  or
              $"p_lat".isNull  or $"d_lat".isNull
          )
          var result = raw_data.filter(
            $"p_lon" <= e_lon and $"p_lon" >= w_lon and
              $"d_lon" <= e_lon and $"d_lon" >= w_lon and
              $"p_lat" <= n_lat and $"p_lat" >= s_lat and
              $"d_lat" <= n_lat and $"d_lat" >= s_lat
          )
          loc_error.write.mode("overwrite").parquet( path_loc_error + file_parquet)
//----------------------------------------------------------------------------------------------------------------------
          // Filter by duration
          val green_taxi_time =  result
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")

          val time_error = green_taxi_time.filter($"duration" < 45)
          time_error.write.mode("overwrite").parquet( path_time_error + file_parquet)

          result = green_taxi_time.filter($"duration" >= 45)
//----------------------------------------------------------------------------------------------------------------------
          // Filter by distance
          val distance_error = result.filter($"trip_distance" <= 0.2)
          distance_error.write.mode("overwrite").parquet(path_distance_error + file_parquet)

          result = result.filter($"trip_distance" > 0.2)
//----------------------------------------------------------------------------------------------------------------------
          // write result
          result.withColumn("total_amount", $"fare_amount" + $"tolls_amount")
            .select(
              $"id",
              $"p_date",
              $"p_time",
              $"p_hour",
              $"duration",
              $"p_lon",
              $"p_lat",
              $"d_lon",
              $"d_lat",
              $"trip_distance",
              $"tolls_amount",
              $"total_amount",
              $"trip_type",
              $"rate_code_id"
            )
            .write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)
//----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + ","  +
            raw_data.count() + "," +
            loc_error.count() + "," +
            time_error.count() + "," +
            distance_error.count() + "," +
            result.count() + "\n")
          fw.close()
        }
        catch {
            case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
              println("Exception: " + year + " " + month + " green taxi data not found.")
              val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
              val date = new Date()


              val file = new File(file_error)
              if (!file.exists) {
                val fw = new FileWriter(file_error)
                fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " green taxi data not found.\n")
                fw.close()
              }else{
                val fw = new FileWriter(file_error, true)
                fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " green taxi data not found.\n")
                fw.close()
              }
        }
      }
    }
  }

  def process_green_taxi_after_2016_07(): Unit = {

    val file_statistic      = java_data_dir + "/green_result_2016_07_2019_12.csv"
    val file_error          = java_data_dir + "/green_errors_2016_07_2019_12.txt"

    val path_time_error     = data_dir + "/green_tripdata/error_time_"
    val path_distance_error = data_dir + "/green_tripdata/error_distance_"
    val path_result         = data_dir + "/green_tripdata/result_"
    val path_raw            = data_dir + "/green_tripdata/green_tripdata_"
    // Create green taxi static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)

    print_Writer.write("Year,Month,Total,Duration,Distance,Result\n")
    print_Writer.close()

    val s_year = 2016
    val e_year = 2019
    val s_month = 1
    val e_month = 12

    for (year <- s_year to e_year) {
      for (int_month <- s_month to e_month) {
        var month = ""
        if (int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try {
          val file_parquet = year + "_" + month + ".parquet"
          //Read in a month's green taxi data align table headings and set id
          val raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(path_raw + year + "-" + month + ".csv")
            .withColumn("id", monotonically_increasing_id())
            .select(
              $"id",
              $"lpep_pickup_datetime".as("p_datetime"),
              $"lpep_dropoff_datetime".as("d_datetime"),
              $"RateCodeID".as("rate_code_id"),
              $"PULocationID".as("p_id"),
              $"DOLocationID".as("d_id"),
              $"trip_distance".as("trip_distance"),
              $"fare_amount".as("fare_amount"),
              $"mta_tax".as("mta_tax"),
              $"tolls_amount".as("tolls_amount"),
              $"trip_type".as("trip_type"),
              $"improvement_surcharge".as("surcharge")
            )

          //----------------------------------------------------------------------------------------------------------------------
          // Filter by duration
          val green_taxi_time = raw_data
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")

          val time_error = green_taxi_time.filter($"duration" < 45)
          time_error.write.mode("overwrite").parquet(path_time_error + file_parquet)

          var result = green_taxi_time.filter($"duration" >= 45)

          //----------------------------------------------------------------------------------------------------------------------
          // Filter by distance
          val distance_error = result.filter($"trip_distance" <= 0.2)
          distance_error.write.mode("overwrite").parquet(path_distance_error + file_parquet)

          result = result.filter($"trip_distance" > 0.2)

          //----------------------------------------------------------------------------------------------------------------------
          // write result
          val green = result.withColumn("total_amount", $"fare_amount" + $"tolls_amount")
            .select(
              $"id",
              $"p_date",
              $"p_time",
              $"p_hour",
              $"duration",
              $"p_id",
              $"d_id",
              $"trip_distance",
              $"tolls_amount",
              $"total_amount",
              $"trip_type",
              $"rate_code_id",
              $"surcharge"
            )

            green
            .write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)

          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            raw_data.count() + "," +
            time_error.count() + "," +
            distance_error.count() + "," +
            result.count() + "\n")
          fw.close()
        }

        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " green taxi data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()
            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " green taxi data not found.\n")
              fw.close()
            } else {
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " green taxi data not found.\n")
              fw.close()
            }
        }

      }
    }
  }

  def process_fhv_before_2017(): Unit ={
    val file_statistic      = java_data_dir + "/fhv_result_2015_01_2017_01.csv"
    val file_error          = java_data_dir + "/fhv_errors_2015_01_2017_01.txt"

    val path_result         = data_dir + "/fhv/fhv_tripdata_2015/result_"
    val path_raw            = data_dir + "/fhv/fhv_tripdata_2015/fhv_tripdata_"
    // Create fhv static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)

    print_Writer.write("Year,Month,all,null,notnull\n")
    print_Writer.close()

    val s_year = 2015
    val e_year = 2017
    val s_month = 1
    val e_month = 12

    for (year <- s_year to e_year) {
      for (int_month <- s_month to e_month) {
        var month = ""
        if (int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try {
          val file_parquet = year + "_" + month + ".parquet"
          //Read in a month's FHV taxi data align table headings and set id
          val raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(path_raw + year + "-" + month + ".csv")
            .withColumn("id", monotonically_increasing_id())
            .select(
              $"id",
              $"Pickup_date".as("p_datetime"),
              $"locationID".as("p_id")
            )

          //----------------------------------------------------------------------------------------------------------------------
          // Partition by date & time
          val fhv_time = raw_data
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))

          var count_is_null = fhv_time.filter($"p_id".isNull).count()
          var count_is_not_null = fhv_time.filter($"p_id".isNotNull).count()
          var count_all = fhv_time.count()
          //----------------------------------------------------------------------------------------------------------------------
          // write result
          fhv_time.select(
              $"id",
              $"p_date",
              $"p_time",
              $"p_hour",
              $"p_id"
            )
            .write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)

          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            count_all + "," +
            count_is_null + "," +
            count_is_not_null +  "\n")
          fw.close()
        }

        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " fhv data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()


            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            } else {
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            }
        }

      }
    }
  }

  def process_fhv_after_2017(): Unit ={
    val file_statistic      = java_data_dir + "/fhv_result_2017_01_2019_12.csv"
    val file_error          = java_data_dir + "/fhv_errors_2017_01_2019_12.txt"

    val path_duration_short = data_dir + "/fhv/fhv_tripdata_2017/error_duration_short_"
    val path_duration_null  = data_dir + "/fhv/fhv_tripdata_2017/error_duration_null_"
    val path_result         = data_dir + "/fhv/fhv_tripdata_2017/result_"
    val path_raw            = data_dir + "/fhv/fhv_tripdata_2017/fhv_tripdata_"
    // Create fhv static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)

    print_Writer.write("year,month,total,duration_short,p_loc_null,p_loc_not_null,result\n")
    print_Writer.close()

    val s_year = 2017
    val e_year = 2019
    val s_month = 1
    val e_month = 12


    for (year <- s_year to e_year) {
      for (int_month <- s_month to e_month) {
        var month = ""
        if (int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try {
          val file_parquet = year + "_" + month + ".parquet"
          //Read in a month's fhv taxi data align table headings and set id
          val file_path = path_raw + year + "-" + month + ".csv"
          var raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(file_path)
          var data = raw_data
          //----------------------------------------------------------------------------------------------------------------------
          //Save 4 common variables and rename different columns
          if(raw_data.columns.contains("Pickup_DateTime")){
            data = data.select(
              $"Pickup_DateTime".as( "p_datetime"),
              $"DropOff_datetime".as("d_datetime"),
              $"PUlocationID".as(    "p_id"),
              $"DOlocationID".as(    "d_id")
            )
          }else if(raw_data.columns.contains("pickup_datetime")){
            data = data.select(
              $"pickup_datetime".as( "p_datetime"),
              $"dropoff_datetime".as("d_datetime"),
              $"PULocationID".as(    "p_id"),
              $"DOLocationID".as(    "d_id")
            )
          }
          raw_data = data
          //----------------------------------------------------------------------------------------------------------------------
          // Partition by date & time and filter by duration
          val fhv_time = raw_data
            .withColumn("id", monotonically_increasing_id())
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")
            .withColumn("d_date", $"d_datetime".cast("date"))
            .withColumn("d_time", date_format($"d_datetime", "HH:mm:ss"))

          val duration_short = fhv_time.filter($"duration" < 45)
          duration_short.write.mode("overwrite").parquet( path_duration_short + file_parquet)

          val result = fhv_time.filter($"duration" >= 45 || $"duration".isNull)

          var count_is_null = result.filter($"p_id".isNull).count()
          var count_is_not_null = result.filter($"p_id".isNotNull).count()

          //----------------------------------------------------------------------------------------------------------------------
          // write result

          result.select(
            $"id",
            $"p_date",
            $"p_time",
            $"p_hour",
            $"d_date",
            $"d_time",
            $"p_id",
            $"d_id"
          ).write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)

          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            raw_data.count() + "," +
            duration_short.count() + "," +
            count_is_null + "," +
            count_is_not_null + "," +
            result.count()+ "\n")
          fw.close()
        }

        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " fhv data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()


            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            } else {
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            }
        }
      }
    }
  }

  def process_hfhv(): Unit ={
    val file_statistic      = java_data_dir + "/fhvhv_result_2019.csv"
    val file_error          = java_data_dir + "/fhvhv_errors_2019.txt"

    val path_duration_short = data_dir + "/fhvhv/error_duration_short_"
    val path_result         = data_dir + "/fhvhv/result_"
    val path_raw            = data_dir + "/fhvhv/fhvhv_tripdata_"
    // Create hfhv static files
    val file_Object = new File(file_statistic)
    val print_Writer = new PrintWriter(file_Object)

    print_Writer.write("year,month,total,duration_short,p_loc_null,p_loc_not_null,result\n")
    print_Writer.close()

    val s_year = 2017
    val e_year = 2019
    val s_month = 1
    val e_month = 12

    for (year <- s_year to e_year) {
      for (int_month <- s_month to e_month) {
        var month = ""
        if (int_month < 10) month = "0" + int_month
        else month = int_month.toString

        try {
          val file_parquet = year + "_" + month + ".parquet"
          //Read in a month's HFHV taxi data align table headings and set id
          val file_path = path_raw + year + "-" + month + ".csv"
          val raw_data = spark.read.format("csv")
            .option("header", "true").option("delimiter", ",")
            .option("inferschema", "true")
            .load(file_path)
            .select(
              $"pickup_datetime".as("p_datetime"),
              $"dropoff_datetime".as("d_datetime"),
              $"PULocationID".as("p_id"),
              $"DOLocationID".as("d_id")
            )

          //----------------------------------------------------------------------------------------------------------------------
          // Partition by date & time and filter by duration
          val fhv_time = raw_data
            .withColumn("id", monotonically_increasing_id())
            .withColumn("p_timestamp", unix_timestamp($"p_datetime"))
            .withColumn("p_date", $"p_datetime".cast("date"))
            .withColumn("p_time", date_format($"p_datetime", "HH:mm:ss"))
            .withColumn("p_hour", date_format($"p_datetime", "HH"))
            .withColumn("d_timestamp", unix_timestamp($"d_datetime"))
            .withColumn("duration", $"d_timestamp" - $"p_timestamp")
            .withColumn("d_date", $"d_datetime".cast("date"))
            .withColumn("d_time", date_format($"d_datetime", "HH:mm:ss"))

          val duration_short = fhv_time.filter($"duration" < 45)
          duration_short.write.mode("overwrite").parquet( path_duration_short + file_parquet)


          val result = fhv_time.filter($"duration" >= 45 || $"duration".isNull)


          var count_is_null = result.filter($"p_id".isNull).count()
          var count_is_not_null = result.filter($"p_id".isNotNull).count()

          //----------------------------------------------------------------------------------------------------------------------
          // write result
          result.select(
            $"id",
            $"p_date",
            $"p_time",
            $"p_hour",
            $"d_date",
            $"d_time",
            $"p_id",
            $"d_id"
          ).write.mode("overwrite")
            .partitionBy("p_date")
            .parquet(path_result + file_parquet)

          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            raw_data.count() + "," +
            duration_short.count() + "," +
            count_is_null + "," +
            count_is_not_null + "," +
            result.count()+ "\n")
          fw.close()
        }
        catch {
          case _: org.apache.spark.sql.AnalysisException =>
            // Display this if exception is found
            println("Exception: " + year + " " + month + " fhv data not found.")
            val formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
            val date = new Date()
            val file = new File(file_error)
            if (!file.exists) {
              val fw = new FileWriter(file_error)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            } else {
              val fw = new FileWriter(file_error, true)
              fw.write(formatter.format(date) + " | Exception: " + year + " " + month + " fhv data not found.\n")
              fw.close()
            }
        }
      }
    }
  }

  def main(args: Array[String]): Unit={
    process_yellow_taxi_before_2017()
//    process_yellow_taxi_after_2017()
//    process_green_taxi_before_2016_07()
//    process_green_taxi_after_2016_07()
//    process_fhv_before_2017()
//    process_fhv_after_2017()
//    process_hfhv()
  }
}