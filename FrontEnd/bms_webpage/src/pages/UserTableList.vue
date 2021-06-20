<template>
  <div class="content">
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-size-66" v-if="this.role==0 ? true : false">
        <new-user-form data-background-color="blue"></new-user-form>
      </div>
      <div class="md-layout-item md-medium-size-100 md-size-66" v-if="this.role!=0 ? true : false">
        <md-card>
          <md-card-header data-background-color="blue">
            <h4 class="title">修改我的密码</h4>
          </md-card-header>
          <md-card-content>
            <md-field>
              <label>旧密码</label>
              <md-input v-model="oldpassword" type="password"></md-input>
            </md-field>

            <md-field>
              <label>新密码</label>
              <md-input v-model="password" type="password"></md-input>
            </md-field>
          </md-card-content>
          <div class="md-layout-item md-size-100 text-right">
            <md-button class="md-raised md-success" v-on:click="modifypassword()">确定</md-button>
          </div>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
        v-if="this.role==0 ? true : false"
      >
        <md-card>
          <md-card-header data-background-color="blue">
            <h4 class="title">用户列表</h4>
            <p class="category"></p>
          </md-card-header>
          <md-card-content>
            <user-table table-header-color="blue"></user-table>
          </md-card-content>
        </md-card>
      </div>

      <!--<div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">进货管理员</h4>
            <p class="category">Here is a subtitle for this table</p>
          </md-card-header>
          <md-card-content>
            <ordered-table></ordered-table>
          </md-card-content>
        </md-card>
      </div>-->
    </div>
  </div>
</template>

<script>
import { NewUserForm } from "@/pages";
import { UserTable } from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  components: {
    UserTable,
    NewUserForm
  },
  data() {
    return {
      role: -1,
      oldpassword: "",
      password: "",
      dialogcontent: "",
      popupdialog: false
    };
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.role = Cookies.get("role");
      }, //Error callback
      response => {
        if (response.status != 200) {
          this.$router.replace({
            path: "/login"
          });
        }
      }
    );
  },
  methods: {
    modifypassword() {
      let sha256 = require("js-sha256").sha256;
      Vue.http
        .get("/editpassword_with_old_password", {
          params: {
            id: Cookies.get("id"),
            oldpassword: sha256(
              this.oldpassword.toString() +
                "jfkH00H8Y3djiojernzwqiy31576Y8hahfhds"
            ),
            newpassword: sha256(
              this.password.toString() + "jfkH00H8Y3djiojernzwqiy31576Y8hahfhds"
            )
          }
        })
        .then(response => {
          if (response.body == "ok") {
            this.dialogcontent = "修改成功";
            this.popupdialog = true;
          } else if (response.body == "-1") {
            this.dialogcontent = "修改失败，旧密码错误";
            this.popupdialog = true;
          } else if (response.body == "failed") {
            this.dialogcontent = "修改失败，服务器错误";
            this.popupdialog = true;
          }
        });
    }
  }
};
</script>
