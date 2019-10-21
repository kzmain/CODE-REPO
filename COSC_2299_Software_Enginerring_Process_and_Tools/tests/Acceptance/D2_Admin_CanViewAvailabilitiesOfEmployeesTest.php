<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D2_Admin_CanViewAvailabilitiesOfEmployeesTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanViewAvailabilitiesOfEmployees()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Availabilities of Employees')
            ->see('Availabilities of Employees');
    }
}
