<template>
  <div class="home">
    <div class="description">
      <h1>Bienvenue sur Grimgar LN</h1>
      <img id="grimgar_logo" src="../assets/Hai_to_Gensō_no_Grimgar_logo.svg"/>
      <img id="main-image" src="../assets/grimgar.jpg"/>
      <p>
        Tout d'abord, Grimgar est une œuvre qui nous charme énormément,
         possédant toutes les qualités pour devenir l'un des plus grands isekai. 
         Malheureusement, l'anime est suspendu et le light novel n'est pas disponible en France. 
         C'est pourquoi nous avons souhaité le traduire afin de vous en faire profiter.
      </p>
    </div>
  </div>
</template>

<style scoped>

.home
{
  background-image: url("../assets/background.jpg") ;
  background-repeat: no-repeat;
  background-size: cover;
  background-color: rgba(0, 0, 0, 0.4);
  background-blend-mode: multiply;
  background-attachment: fixed;
  height: 100%;
}
h1
{
 text-align: center;
 color : #9e2b34;
 text-decoration: underline;
}

.home p
{
  color : #9e2b34;
  font-size: 25px;
  font-weight: bold;
  padding: 20px;
  margin : 0 40px;
}

.description
{
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  margin : 0 auto;
  background-color: #181818;
  width : 50%;
  height: max-content;
  justify-content: center;
}

#grimgar_logo
{
  width: 60%;
  margin : 0 auto;
  display : flex;
  border-radius: 5px;
  filter: invert(21%) sepia(67%) saturate(1506%) hue-rotate(325deg) brightness(99%) contrast(97%);
}

#main-image
{
  width: 60%;
  margin : 10px auto;
  display : flex;
  border-radius: 5px;
}

</style>
