<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class LoginWrongEmailTest extends DuskTestCase
{
    /**
     * A Dusk test example.
     *
     * @return void
     */
    public function testExample()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->type('email','whye9433@gmail.com')
			->type('password','ábcdefg')		    
			->press('Login')
		   	->assertSee('These credentials do not match our records');
        });
    }
}
