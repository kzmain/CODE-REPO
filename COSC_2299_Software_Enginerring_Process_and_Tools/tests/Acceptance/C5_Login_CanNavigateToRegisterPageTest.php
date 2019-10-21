<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class C5_Login_CanNavigateToRegisterPageTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanNavigateToRegisterPage()
    {
        $this->visit('/login')
            ->type('steve@apple.com', 'email')
            ->click('Register')
            ->seePageIs('/register');
    }
}
