<template>
  <form
    style="width:500px;height:350px;margin-top:-250px;margin-left:-250px;position:absolute;top:50%;left:50%;"
  >
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />

    <center>
      <h3>欢迎使用进销存系统</h3>
    </center>
    <md-card>
      <md-card-header data-background-color="blue">
        <h4 class="title">用户登录</h4>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
              <label>用户名</label>
              <md-input v-model="username" type="text" @keyup.enter="loginprocess"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-100">
            <md-field>
              <label>密码</label>
              <md-input v-model="password" type="password" @keyup.enter="loginprocess"></md-input>
            </md-field>
          </div>

          <div class="md-layout-item md-size-100 text-right">
            <md-button class="md-primary" v-on:click="loginprocess()">登录</md-button>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </form>
</template>
<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "login",
  data() {
    return {
      dialogcontent: "",
      popupdialog: false,
      username: "",
      password: ""
    };
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.redirtopage(Cookies.get("role"));
      },
      function() {}
    );
  },
  methods: {
    loginprocess() {
      let sha256 = require("js-sha256").sha256;
      Vue.http
        .get("/login", {
          params: {
            username: this.username,
            password: sha256(
              this.password.toString() + "jfkH00H8Y3djiojernzwqiy31576Y8hahfhds"
            )
          }
        })
        .then(
          response => {
            if (response.body.result == 1) {
              Cookies.set("id", response.body.id);
              Cookies.set("token", response.body.token);
              Cookies.set("username", this.username);
              Cookies.set("role", response.body.role);
              this.redirtopage(Number(response.body.role));
            } else {
              window.console.log("ddd");
              this.dialogcontent = "用户名或密码错误";
              this.popupdialog = true;
            }
          },
          response => {
            this.dialogcontent = "登录失败，服务器API故障";
            this.popupdialog = true;
          }
        );
    },
    redirtopage(role) {
      if (role == 0) {
        this.$router.replace({
          path: "/dashboard"
        });
      } else if (role == 1) {
        this.$router.replace({
          path: "/storetable"
        });
      } else if (role == 2) {
        this.$router.replace({
          path: "/importtable"
        });
      } else if (role == 3) {
        this.$router.replace({
          path: "/saletable"
        });
      } else if (role == 4) {
        this.$router.replace({
          path: "/storetable"
        });
      } else if (role == 5) {
        this.$router.replace({
          path: "/saletable"
        });
      }
      window.location.reload();
    }
  }
};
</script>
<style></style>
