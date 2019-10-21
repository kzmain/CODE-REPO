<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D6_Admin_CanMakeNewBookingTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanMakeNewBooking()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('New Booking')
            ->see('New Booking')
            ->press('View Availability')
            ->click('123-223')
            ->see('Booking successful!');
    }
}
