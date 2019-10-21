<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D4_Admin_CanViewSummaryOfPastBookingsTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanViewSummaryOfPastBookings()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Summary of Past Bookings')
            ->see('Summary of Past Bookings');
    }
}
