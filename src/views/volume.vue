<script >
import { ref } from 'vue';
import { useRoute } from "vue-router";
import Chap_Card from "../components/chapter_card.vue"
export default{
    name : "volume",
    components:
    {
        Chap_Card
    },
    setup()
    {
        const volume_details = ref(Object)
        const route = useRoute();
        const init = async ()=>
        {
            volume_details.value = await(await fetch(`/api/volumes-info=${route.params.vol_num}`)).json();
            console.log(volume_details.value)
        }


        return{
            init,
            volume_details
        }
    },

    beforeMount()
    {
        this.init();
    }
}

</script>

<template>
    <div class="volume">
        <div class="volume-detail">
            <h1>Volume {{ $route.params.vol_num }} : {{ this.volume_details.Name }}</h1>
            <div class="details-container">
               <div class="details-item"><img id="cover" :src="`/api/cover/${$route.params.vol_num }`"/></div>
               <div class="details-item">
                    <p> <span style="font-style: italic;"> <span style="text-decoration: underline; ;">Description :</span>  {{ this.volume_details.Description }} </span></p>
                    <span class="sub-details">
                        <p id="released"> Sortie le : {{ this.volume_details.Released }}</p>
                        <p id="comment"> Commentaires : {{ this.volume_details.CommentNum }}</p>
                    </span>
                    
               </div>
            </div>
            <hr size="3" color="white" width="90%">
            <div>
                <h2>Liste des chapitres</h2>
                <Chap_Card v-for="(chap, index) in this.volume_details.Chapter"
                v-bind:key="index"
                v-bind:Chapter_Name_Prop="chap.ChapterName"
                v-bind:ChapNum_Prop = "chap.ChapterNum"
                v-bind:Vol_Num_Prop = "$route.params.vol_num"
                v-bind:CommentNum_Prop = "chap.CommentNum"
                v-bind:Completed_Percent_Prop="0"
                />
            </div>

        </div>
    </div>
</template>

<style scoped>
.volume{
    height: 100%;
    background-image: url("../assets/background2.jpg") ;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    height: max-content;
    background-color: rgba(0, 0, 0, 0.4);
    background-blend-mode: multiply;
}

.volume-detail
{
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    margin : 0 auto;
    background-color: #181818;
    width : 60%;
    height: max-content;
    justify-content: center;
    color : white;
    font-size: 20px;
}

.details-container
{
    display: flex;
    flex-direction: row;
    width : 90%;
    margin : 0 auto;
}

h2{
    text-align: center;
    text-decoration: underline;
}

.sub-details
{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

#released
{
    align-self: flex-start;
}

#comment
{
    align-self: flex-end;
}

.details-item
{
    display: flex;
    margin : 10px 20px;
    flex-direction: column;
}
h1{
    text-align: center;
    color : white;
    text-decoration: underline;
}

#cover
{
    border-radius: 25px;
    margin : 10px 0;
    user-select: none;
}
</style>