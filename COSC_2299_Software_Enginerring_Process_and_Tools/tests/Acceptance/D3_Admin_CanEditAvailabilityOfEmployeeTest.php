<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D3_Admin_CanEditAvailabilityOfEmployeeTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanEditAvailabilityOfEmployee()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Availabilities of Employees')
            ->see('Availabilities of Employees')
            ->click('None')
            ->see('Update Availability')
            ->type('123', 'start_time')
            ->type('321', 'end_time')
            ->press('Update Availability')
            ->see('123-321');
    }
}
