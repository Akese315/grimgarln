
<script>
import { toRef } from '@vue/reactivity';
import {RouterLink} from 'vue-router'
export default {
    name: "vol_card",
    props :
    {
        Vol_Name_Prop : String,
        Vol_Num_Prop : Number,
        Chap_Num_Prop : Number,
        CommentNum_Prop : Number
    },
    setup(props)
    {
        const Vol_Name = toRef(props, "Vol_Name_Prop");
        const Vol_Num = toRef(props, "Vol_Num_Prop");
        const Chap_Num = toRef(props, "Chap_Num_Prop");
        const CommentNum = toRef(props, "CommentNum_Prop");


        return{
            Vol_Name,
            Chap_Num,
            CommentNum,
            Vol_Num
        }
    }
};

</script>

<template>
    
    <div class="card">
        <RouterLink :to="`/volume/${ this.Vol_Num }/`">
        <img id ="cover" class="card-item" :src="`https://grimgarln.fr/api/cover/${this.Vol_Num}`"/>
        </RouterLink>
        <span id ="vol_name" class="card-item">{{ this.Vol_Name }}</span>
        <span id ="chap_num" class="card-item">chapitres : {{ this.Chap_Num }}</span>
        <span id ="comment_num" class="card-item"><img src="../assets/comment-icon.svg"/>{{ this.CommentNum }}</span>
    </div>

</template>

<style scoped>
    .card{
        background-color: #4a4a4a ;
        border-radius: 8px;
        width: 80%;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-gap: 10px;
        padding: 10px;
        font-weight: bold;
        color:#ffffff;
        font-size: 20px;
        margin: 20px auto;
        align-items: center;
    }

    .card-item
    {
        padding: 20px;
        text-align: center;
    }

    #comment_num img
    {
        position : relative;
        vertical-align: middle;
        margin : 3px;
        height: 1em;
        width: 1em;
        filter: invert(100%) sepia(1%) saturate(7500%) hue-rotate(158deg) brightness(117%) contrast(100%);
        
    }
    #cover
    {
        border-radius: 5px;
        width : 8em;
        padding : 0;
        transition : 0.5s;
    }

    #cover:hover
    {
       transform : translateX(20px)
    }

    a
    {
        color : white;
        text-decoration: none;
    }


</style>