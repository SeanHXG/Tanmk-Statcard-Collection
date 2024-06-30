import React, { useEffect, useState } from 'react'
import 'bootstrap/dist/css/bootstrap.css'
import $ from 'jquery'

function HomePage(props) {

    useEffect(() => {
        $.ajax({
            url: 'http://127.0.0.1:8000/recipes/',
            method: 'Get',
            success: function(xhr){
            },
            error: function(xhr){
                console.log(xhr)
            }
        })
    }, [])

    return(
        <>
        <SearchHeader searchParams={props.searchParams} setSearchParams={props.setSearchParams} />
        <div className='container-fluid carousel-table'>
            <div className='row'>
                <div className='col recipe-col'> <HomeRecipeCarousel category='0' cardInfo={breakfast} key='Breakfast_Carousel' searchParams={props.searchParams} setSearchParams={props.setSearchParams} /> </div>
                <div className='col recipe-col'> <HomeRecipeCarousel category='1' cardInfo={lunch} key='Lunch_Carousel' searchParams={props.searchParams} setSearchParams={props.setSearchParams} /> </div>
                <div className='col recipe-col'> <HomeRecipeCarousel category='2' cardInfo={dinner} key='Dinner_Carousel' searchParams={props.searchParams} setSearchParams={props.setSearchParams} /> </div>
            </div>
            <div className='row'>
                <div className='col recipe-col'> <HomeRecipeCarousel category='3' cardInfo={popular} key='Popular_Carousel' searchParams={props.searchParams} setSearchParams={props.setSearchParams} /> </div>
            </div>
        </div>
        </>
    );
}

export default HomePage