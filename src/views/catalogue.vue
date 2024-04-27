<template>
    <div class="catalogue">
        <div id="list">
            <h1>Liste des volumes</h1>
            <Vol_Card v-for="(vol, index) in this.Catalogue "
            v-bind:key="index"
            v-bind:Vol_Name_Prop="vol.Name"
            v-bind:Chap_Num_Prop = "vol.ChapterNum"
            v-bind:Vol_Num_Prop = "vol.Volume"
            v-bind:CommentNum_Prop = "vol.CommentNum"
            />
        </div>
    </div>
  </template>
  
<style scoped>

h1
{
 text-align: center;
 color : whitesmoke;
}

#list
{
    border-radius: 10px;
  display: flex;
  flex-direction: column;
  margin : 0 auto;
  background-color: #181818;
  width : 60%;
  height: max-content;
  justify-content: center;
}

.catalogue p
{
  color : whitesmoke;
  font-size: 20px;
  padding: 20px;
}

.catalogue
{
  background-image: url("../assets/background2.jpg") ;
  background-repeat: no-repeat;
  background-size: cover;
  height: max-content;
  background-color: rgba(0, 0, 0, 0.4);
  background-blend-mode: multiply;
  background-attachment: fixed;
  height: 100%;
}

h1
{
 text-align: center;
}
  
</style>
  
<script>
import Vol_Card from '../components/volume_card.vue'
import { ref } from 'vue';
export default {
    name : "catalogue",
    components :
    {
      Vol_Card,
    },
    setup()
    {
      var Catalogue = ref(new Array);


      const setVolumes = async (volum_num)=>
      {
        for(var i = 1; i<=volum_num; i++)
        {
          const data = await(await fetch(`/api/volumes-info=${i}`)).json();
          Catalogue.value.push(data)
        }

        console.log(Catalogue.value)
      }


      return {
        setVolumes,
        Catalogue
      }
    },
    beforeMount()
    {
      fetch("/api/volumes"
      ).then(response=> response.json()).then(data=>{
        this.setVolumes(data.volume_num)
      }).catch(error=>
      {
        //console.error(error);
      });
    }
};

</script>