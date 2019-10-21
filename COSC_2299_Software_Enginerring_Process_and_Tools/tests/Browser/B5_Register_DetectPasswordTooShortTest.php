<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class B5_Register_DetectPasswordTooShortTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testB5_Register_DetectPasswordTooShort()
    {
        $this->browse(function ($browser) {
            $browser->visit('/register')
                    ->type('name', 'Bill Gates')
                    ->type('address', '1 Main St')
                    ->type('city', 'Seattle')
                    ->select('state', 'NSW')
                    ->type('postcode', '2000')
                    ->type('phone', '0412345678')
                    ->type('email', 'bill@microsoft.com')
                    ->type('password', 'aA1')
                    ->type('password_confirmation', 'aA1')
                    ->press('Register')
                    ->assertSee('The password must be at least 6 characters');
        });
    }
}
