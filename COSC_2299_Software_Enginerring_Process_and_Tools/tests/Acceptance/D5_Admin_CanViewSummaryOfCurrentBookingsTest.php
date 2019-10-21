<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D5_Admin_CanViewSummaryOfCurrentBookingsTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanViewSummaryOfCurrentBookingsTest()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Summary of Current Bookings')
            ->see('Summary of Current Bookings');
    }
}
