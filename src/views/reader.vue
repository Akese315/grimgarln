<script>
import { ref } from 'vue';
import { useRoute } from "vue-router";
import {RouterLink} from 'vue-router'
import {APP_URL }from '../constants'
export default {
    name : "reader",
    setup()
    {
        const text = ref(Array);
        const route = useRoute();
        fetch(`${APP_URL}/api/vol/${route.params.vol_num}/chap/${route.params.chap_num}`)
        .then(ponse=> ponse.json())
        .then(data=>{
            text.value = data.Text;
            console.log(text.value)
        })
        .catch(error=>
        {
            //console.error(error);
        });
        return{
            text,
            route
        }
    }
}
</script>

<template>
    <div class="image-container">
        <button v-if="parseInt(route.params.chap_num) > 0"><RouterLink :to="`/volume/${ route.params.vol_num }/chap/${parseInt(route.params.chap_num)-1}`">Precedent</RouterLink> </button>
        <button><RouterLink :to="`/volume/${ route.params.vol_num }/chap/${parseInt(route.params.chap_num) +1 }`">Suivant</RouterLink></button>
        <div class="reader-container" v-html="this.text"></div>
    </div>
    
</template>


<style scoped>
    h1{
        text-align: center;
    }

    .comment{
        color : rgb(141, 206, 215);
    }
    
    .italic
    {
        color : red;
    }


    .reader-container
    {
        background-color: rgb(63, 63, 63);
        height: max-content;
        width : max-content;
        margin : 0 auto;
        padding :10px;
        color : white;
    }

    .image-container{
        width: 100%;
        height: max-content;
        min-height: 87%;
        padding : 0;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        background-color: rgb(92, 92, 92);
        background-blend-mode: multiply;
    }

</style>