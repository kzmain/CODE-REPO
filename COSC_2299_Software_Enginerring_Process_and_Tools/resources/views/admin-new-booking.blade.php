@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
                                        @if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
                                        @endif
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">New Booking</div>


                <div class="panel-body">
                    <form class="form-horizontal" role="form" method="POST" action="{{ url('admin-new-booking') }}">
                        {{ csrf_field() }}

            <div class="form-group">
                <label for="task" class="col-sm-3 control-label">Customer</label>

                <div class="col-sm-6">
<select name="user_id" id="user_id" class="form-control">
                                @foreach ($users as $user)
<option value="{{$user->id}}">{{$user->name}}</option>
                                @endforeach
</select>
                </div>
            </div>

            <div class="form-group">
                <label for="task" class="col-sm-3 control-label">Service</label>

                <div class="col-sm-6">
<select name="service_id" id="service_id" class="form-control">
                        @foreach ($services as $service)
<option value="{{$service->id}}">{{$service->name}}</option>
                        @endforeach
</select>
                </div>
            </div>

                        <div class="form-group">
                            <div class="col-md-6 col-md-offset-4">
                                <button type="submit" class="btn btn-primary">
                                   View Availability 
                                </button>
                            </div>
                        </div>
                    </form>

<p>
<br>
<a href="/home">Home</a>
</p>

                </div>
            </div>
        </div>
    </div>
</div>
@endsection
