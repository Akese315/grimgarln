
<script>
import {RouterLink} from 'vue-router'
export default {
  data() {
    return {
     
    };
  }
};

</script>

<template>
    <nav>
      <ul>
        <li><RouterLink to="/">Menu</RouterLink></li>
        <li><RouterLink to="/catalogue">Catalogue</RouterLink></li>
      </ul>
    </nav>
</template>

<style scoped>

ul{
    list-style-type: none;
    text-align: center;
    padding: 0;
    margin-top: 0;
    margin-bottom: 0;
}
ul li{
    padding : 10px 40px;
    display: inline-block;
}

a
{
    color : white;
}

nav{
  background-color: #181818;
  font-size: 30px;
  padding: 10px;
}

</style>