<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class B3_Register_DetectDuplicateUseridTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testB3_Register_DetectDuplicateUserid()
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
                    ->type('password', 'aA1aA1')
                    ->type('password_confirmation', 'aA1aA1')
                    ->press('Register')
                    ->assertSee('The email has already been taken');
        });
    }
}
