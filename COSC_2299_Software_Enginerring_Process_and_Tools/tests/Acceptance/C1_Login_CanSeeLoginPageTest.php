<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class C1_Login_CanSeeLoginPageTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanSeeLoginPage()
    {
        $this->visit('/login')
            ->see('Login');
    }
}
