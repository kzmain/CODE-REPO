<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class C4_Login_CanNavigateToForgotYourPasswordPageTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanNavigateToForgotYourPasswordPage()
    {
        $this->visit('/login')
            ->type('steve@apple.com', 'email')
            ->click('Forgot Your Password?')
            ->seePageIs('/password/reset');
    }
}
