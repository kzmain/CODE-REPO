<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D1_Admin_CanAddEmployeeTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanAddEmployee()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Add Employee')
            ->see('Add Employee')
            ->type('Random Joe', 'name')
            ->type('1 Main Street', 'address')
            ->type('Disneyland', 'city')
            ->select('NSW', 'state')
            ->type('2000', 'postcode')
            ->type('0412345678', 'phone')
            ->type('randomjoe@example.com', 'email')
            ->press('Add Employee')
            ->see('Random Joe was added as an employee');
    }

}
