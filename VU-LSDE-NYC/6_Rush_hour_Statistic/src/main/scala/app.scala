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
//
//  // Bounds to filter trips out of NYC
//  val w_lon: Double = -74.2463  //左 left bound
//  val e_lon: Double = -73.7141  //右 right bound
//  val n_lat: Double = 40.9166   //上 up bound
//  val s_lat: Double = 40.4767   //下 down bound


  def process_yellow_taxi_2018(): Unit ={
    val file_statistic      = java_data_dir + "/yellow_result_rush_hour_statistic_2018.csv"
    val file_error          = java_data_dir + "/yellow_result_rush_hour_statisti_2018.txt"

//    val path_time_error     = data_dir + "/yellow_tripdata/error_time_"
//    val path_distance_error = data_dir + "/yellow_tripdata/error_distance_"
//    val path_result         = data_dir + "/yellow_tripdata/result_"
//    val path_raw            = data_dir + "/yellow_tripdata/yellow_tripdata_"
    // Create yellow taxi static files
//    val file_Object = new File(file_statistic)
//    val print_Writer = new PrintWriter(file_Object)
//    print_Writer.write("Year,Month,Total,Duration,Distance,Result\n")
//    print_Writer.close()

    val year = 2018
    val e_year = 2018
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
          //2018's heading change to standard table heading
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
          // select surcharge
          raw_data.select($"surcharge")
            .write.mode("overwrite")
            .groupBy("p_hour")
            .csv(path_result + file_parquet)
          //----------------------------------------------------------------------------------------------------------------------
          //write static files
          val fw = new FileWriter(file_statistic, true)
          fw.write(year + "," + month + "," +
            raw_data.count())
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




  def main(args: Array[String]): Unit={
//    process_yellow_taxi_before_2017()
    process_yellow_taxi_2018()
//    process_green_taxi_before_2016_07()
//    process_green_taxi_after_2016_07()
//    process_fhv_before_2017()
//    process_fhv_after_2017()
//    process_hfhv()
  }
}