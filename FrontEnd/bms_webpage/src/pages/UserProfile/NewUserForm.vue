<template>
  <form>
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />
    <md-card>
      <md-card-header :data-background-color="dataBackgroundColor">
        <h4 class="title">新用户</h4>
        <p class="category">创建新用户</p>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>用户名</label>
              <md-input v-model="username" type="text"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>密码</label>
              <md-input v-model="password" type="password"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-50">
            <md-field>
              <label>角色</label>
              <md-select v-model="role">
                <md-option value="0">系统管理员</md-option>
                <md-option value="1">库存管理员</md-option>
                <md-option value="2">进货管理员</md-option>
                <md-option value="3">销售管理员</md-option>
                <md-option value="4">入库员</md-option>
                <md-option value="5">销售员</md-option>
              </md-select>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100 text-right">
            <md-button class="md-raised md-success" v-on:click="newuser($event)">创建用户</md-button>
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
  name: "new-user-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      dialogcontent: "",
      popupdialog: false,
      username: null,
      password: null,
      role: 0
    };
  },
  methods: {
    newuser: function(e) {
      let sha256 = require("js-sha256").sha256;
      Vue.http
        .get("/newuser", {
          params: {
            username: this.username,
            password: sha256(this.password.toString() + "jfkH00H8Y3djiojernzwqiy31576Y8hahfhds"),
            role: this.role
          }
        })
        .then(response => {
          window.console.log(response.body);
          if (response.body == "ok") {
            this.dialogcontent = "创建成功";
            this.dialogDismiss = function() {
              location.reload();
              this.dialogDismiss = function() {};
            };
            this.popupdialog = true;
          } else {
            this.dialogcontent = "创建失败";
            this.popupdialog = true;
          }
        });
    },
    dialogDismiss: function() {}
  },
  watch: {
    popupdialog: {
      handler(newName, oldName) {
        if (newName == false) {
          this.dialogDismiss();
        }
      }
    }
  }
};
</script>
<style></style>
