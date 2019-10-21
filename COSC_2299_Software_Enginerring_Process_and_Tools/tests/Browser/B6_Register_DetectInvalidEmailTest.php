<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class B6_Register_DetectInvalidEmailTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testB6_Register_DetectInvalidEmail()
    {
        $this->browse(function ($browser) {
            $browser->visit('/register')
                    ->type('name', 'Bill Gates')
                    ->type('address', '1 Main St')
                    ->type('city', 'Seattle')
                    ->select('state', 'NSW')
                    ->type('postcode', '2000')
                    ->type('phone', '0412345678')
                    ->type('email', 'bill@microsoft')
                    ->type('password', 'aA1')
                    ->type('password_confirmation', 'aA1')
                    ->press('Register')
                    ->assertSee('The email must be a valid email address');
        });
    }
}
