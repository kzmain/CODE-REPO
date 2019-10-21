<?php

use App\Business;
use App\Service;
use App\User;
use App\Employee;
use App\Availability;
use App\Booking;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('businesses')->delete();
        DB::table('services')->delete();
        DB::table('users')->delete();
        DB::table('employees')->delete();
        DB::table('availabilities')->delete();
        DB::table('bookings')->delete();

        $business = Business::create(array(
            'name' => "Dr. Nick's Supercheap Medical Centre"
        ));

        $services = array();
        $services[] = Service::create(array(
            'name' => 'Lobotomy',
            'duration_in_minutes' => 60
        ));
        $services[] = Service::create(array(
            'name' => 'Brain Transplant',
            'duration_in_minutes' => 45
        ));
        $services[] = Service::create(array(
            'name' => 'Liver Transplant',
            'duration_in_minutes' => 90
        ));
        $services[] = Service::create(array(
            'name' => 'Routine Checkup',
            'duration_in_minutes' => 120
        ));
        $services[] = Service::create(array(
            'name' => 'Heart Transplant',
            'duration_in_minutes' => 30
        ));

        $users = array();
        $users[] = User::create(array(
            'name' => 'Debug',
            'address' => '1 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0412345678',
            'business_id' => $business->id,
            'email' => 'debug@example.com',
            'password' => bcrypt('Debug1')
        ));
        $users[] = User::create(array(
            'name' => 'Admin',
            'address' => '1 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0412345678',
            'business_id' => $business->id,
            'email' => 'admin@example.com',
            'password' => bcrypt('Admin1')
        ));
        $namesForUsers = array('Agnes', 'Paula', 'Denise', 'Christy', 'Steve', 'Paul', 'Joe', 'Chris', 'Adam', 'Rachel', 'Manny', 'Larry', 'Moe', 'Jack', 'Sara', 'Bruce');
        foreach ($namesForUsers as $name) {
            $users[] = User::create(array(
                'name' => $name,
                'address' => '1 Main St',
                'city' => 'Melbourne',
                'state' => 'VIC',
                'postcode' => '3000',
                'phone' => '0412345678',
                'email' => strtolower($name . '@example.com'),
                'password' => bcrypt('Password1')
            ));
        }

        $employees = array();
        $employees[] = Employee::create(array(
            'name' => 'Dr. Evil',
            'address' => '1 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0400000001',
            'business_id' => $business->id,
            'email' => 'drevil@hotmail.com'
        ));
        $employees[] = Employee::create(array(
            'name' => 'Dr. Nick',
            'address' => '5 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0400000005',
            'business_id' => $business->id,
            'email' => 'drnick@hotmail.com'
        ));
        $employees[] = Employee::create(array(
            'name' => 'Dr. Hannibal Lecter',
            'address' => '2 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0400000002',
            'email' => 'hannibal@gmail.com',
            'business_id' => $business->id
        ));
        $employees[] = Employee::create(array(
            'name' => 'Dr. Henry Jekyll',
            'address' => '3 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0400000003',
            'email' => 'drjekyll@yahoo.com',
            'business_id' => $business->id
        ));
        $employees[] = Employee::create(array(
            'name' => 'Dr. Henry Frankenstein',
            'address' => '4 Main St',
            'city' => 'Melbourne',
            'state' => 'VIC',
            'postcode' => '3000',
            'phone' => '0400000004',
            'email' => 'drfrankenstein@gmail.com',
            'business_id' => $business->id
        ));

        for ($i=1; $i<=2; $i++) {
            Availability::create(array(
                'employee_id' => $employees[0]->id,
                'day_of_week' => $i,
                'start_time' => 700+$i*100,
                'end_time' => 1100+$i*100
            ));
        }
        for ($i=2; $i<=3; $i++) {
            Availability::create(array(
                'employee_id' => $employees[1]->id,
                'day_of_week' => $i,
                'start_time' => 900+$i*100,
                'end_time' => 1200+$i*100
            ));
        }
        for ($i=3; $i<=4; $i++) {
            Availability::create(array(
                'employee_id' => $employees[2]->id,
                'day_of_week' => $i,
                'start_time' => 1000+$i*100,
                'end_time' => 1300+$i*100
            ));
        }
        for ($i=4; $i<=5; $i++) {
            Availability::create(array(
                'employee_id' => $employees[3]->id,
                'day_of_week' => $i,
                'start_time' => 700+$i*100,
                'end_time' => 1100+$i*100
            ));
        }
        for ($i=5; $i<=6; $i++) {
            Availability::create(array(
                'employee_id' => $employees[4]->id,
                'day_of_week' => $i,
                'start_time' => 900+$i*100,
                'end_time' => 1200+$i*100
            ));
        }
    }
}

