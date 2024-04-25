
<script>
import { toRef } from '@vue/reactivity';
import {RouterLink} from 'vue-router'
export default {
    name: "chap_card",
    props :
    {
        Completed_Percent_Prop : Number,
        CommentNum_Prop : Number,
        Vol_Num_Prop : String,
        ChapNum_Prop : Number,
        Chapter_Name_Prop : String
    },
    setup(props)
    {
        const Chapter_Name = toRef(props, "Chapter_Name_Prop");
        const ChapNum = toRef(props, "ChapNum_Prop");
        const Completed_Percent = toRef(props, "Completed_Percent_Prop");
        const Vol_Num = toRef(props, "Vol_Num_Prop");
        const CommentNum = toRef(props, "CommentNum_Prop");


        return{
            Chapter_Name,
            Completed_Percent,
            CommentNum,
            Vol_Num,
            ChapNum
        }
    }
};

</script>

<template>
     <RouterLink :to="`/volume/${ this.Vol_Num }/chap/${this.ChapNum}`">
        <div class="card">
            <p id="chap_num" class="card-item">#{{ this.ChapNum }}</p>
            <p id ="chap_name" class="card-item">{{ this.Chapter_Name }}</p>
            <p id ="comment_num" class="card-item"><img src="../assets/comment-icon.svg"/>{{ this.CommentNum }}</p>
            <p id ="completed_percent" class="card-item">{{ this.Completed_Percent }}%</p>
        </div>
    </RouterLink>
</template>

<style scoped>
    .card{
        background-color: #4a4a4a ;
        border-radius: 8px;
        width: 80%;
        display: grid;
        grid-template-columns: 1fr 4fr 1fr 1fr;
        grid-gap: 10px;
        padding: 5px;
        font-weight: bold;
        
        font-size: 20px;
        margin: 20px auto;
        align-items: center;
    }
    
    .card:hover #chap_num{
        color : #9e2b34;
    }

    #chap_name
    {
        text-overflow:ellipsis;
        max-height: 1em;
        overflow: hidden;
        white-space: nowrap; 
    }

    #chap_num
    {
       width: max-content;
       font-size: 35px;
    }
    
    .card-item
    {
        padding: 20px;
        overflow: hidden;
        margin :0;
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

    a{
        color : white;
        text-decoration: none;
    }

    


</style>