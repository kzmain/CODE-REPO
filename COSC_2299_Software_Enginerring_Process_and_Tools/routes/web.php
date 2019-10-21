<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

use Illuminate\Http\Request;

use App\User;
use App\Employee;
use App\Business;
use App\Availability;

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', 'HomeController@index');
Route::get('/delete-availability/{employee_id}/{day_of_week}', 'AvailabilityController@handleDeleteAvailability');
Route::post('/update-availability', 'AvailabilityController@handleUpdateAvailability');
Route::get('/update-availability/{employee_id}/{day_of_week}', 'AvailabilityController@updateAvailability');
Route::get('/show-availabilities-for-each-employee', 'EmployeeController@showAvailabilitiesForEachEmployee');
Route::get('/add-employee', 'EmployeeController@addEmployee');
Route::post('/handle-add-employee', 'EmployeeController@handleAddEmployee');
Route::get('/summary-of-past-bookings','BookingController@summaryOfPastBookings');
Route::get('/summary-of-current-bookings','BookingController@summaryOfCurrentBookings');
Route::post('/admin-new-booking', 'BookingController@postNewBooking');
Route::get('/admin-new-booking', 'BookingController@getNewBooking');
Route::get('/view-booking-availability/{user_id}/{service_id}', 'BookingController@getViewBookingAvailability');
Route::get('/make-new-booking/{user_id}/{service_id}/{employee_id}/{day_of_week}/{start_time}', 'BookingController@makeNewBooking');
Route::get('/home/filter','BookingController@bookingFilter');
Route::get('/add-service', 'ServiceController@addService');
Route::post('/handle-add-service', 'ServiceController@handleAddService');

/*
 * Debugging
 */

Route::post('/debug/choose-view-available', 'DebugController@postChooseViewAvailable');
Route::get('/debug/choose-view-available', 'DebugController@getChooseViewAvailable');
Route::get('/debug/booking-employee/{employee_id}', 'DebugController@getBookingEmployee');
Route::get('/debug/booking-user/{user_id}', 'DebugController@getBookingUser');
Route::post('/debug/make-new-booking/{user_id}/{service_id}/{employee_id}/{day_of_week}/{start_time}', 'DebugController@makeNewBooking');
Route::get('/debug/make-new-booking/{user_id}/{service_id}/{employee_id}/{day_of_week}/{start_time}', 'DebugController@makeNewBooking');
Route::get('/debug/confirm-new-booking/{user_id}/{service_id}/{employee_id}/{day_of_week}/{start_time}', 'DebugController@confirmNewBooking');
Route::get('/debug/view-available/{user_id}/{service_id}', 'DebugController@viewAvailable');
Route::get('/debug/delete-booking/{id}', 'DebugController@deleteBooking');
Route::post('/debug/booking', 'DebugController@postBooking');
Route::get('/debug/booking', 'DebugController@getBooking');
Route::get('/debug/delete-service/{id}', 'DebugController@deleteService');
Route::post('/debug/service', 'DebugController@postService');
Route::get('/debug/service', 'DebugController@getService');
Route::get('/debug/delete-availability/{id}', 'DebugController@deleteAvailability');
Route::post('/debug/availability', 'DebugController@postAvailability');
Route::get('/debug/availability', 'DebugController@getAvailability');
Route::get('/debug/delete-business/{id}', 'DebugController@deleteBusiness');
Route::post('/debug/business', 'DebugController@postBusiness');
Route::get('/debug/business', 'DebugController@getBusiness');
Route::get('/debug/delete-employee/{id}', 'DebugController@deleteEmployee');
Route::get('/debug/employee', 'DebugController@getEmployee');
Route::get('/debug/make-user-admin/{id}', 'DebugController@makeUserAdmin');
Route::get('/debug/make-user-customer/{id}', 'DebugController@makeUserCustomer');
Route::get('/debug/user', 'DebugController@getUser');

