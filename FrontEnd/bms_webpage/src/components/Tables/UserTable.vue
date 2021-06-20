<template>
  <div>
    <md-dialog :md-active.sync="modifydialog.show">
      <md-dialog-title>编辑用户(ID={{modifydialog.itemdata.id}})</md-dialog-title>

      <div style="padding:20px;">
        <md-field>
          <label>用户名</label>
          <md-input v-model="modifydialog.itemdata.username"></md-input>
        </md-field>
        <md-field>
          <label>状态</label>
          <md-select v-model="modifydialog.itemdata.role">
            <md-option value="0">系统管理员</md-option>
            <md-option value="1">库存管理员</md-option>
            <md-option value="2">进货管理员</md-option>
            <md-option value="3">销售管理员</md-option>
            <md-option value="4">入库员</md-option>
            <md-option value="5">销售员</md-option>
          </md-select>
        </md-field>
      </div>
      <md-dialog-actions>
        <md-button class="md-primary" @click="modifydialog.show = false">取消</md-button>
        <md-button class="md-primary" @click="confirmModifyItem">确定</md-button>
      </md-dialog-actions>
    </md-dialog>

    <md-dialog :md-active.sync="passworddialog.show">
      <md-dialog-title>修改密码(ID={{passworddialog.id}})</md-dialog-title>

      <div style="padding:20px;">
        <md-field>
          <label>新密码</label>
          <md-input v-model="passworddialog.newpassword" type="password"></md-input>
        </md-field>
      </div>
      <md-dialog-actions>
        <md-button class="md-primary" @click="passworddialog.show = false">取消</md-button>
        <md-button class="md-primary" @click="confirmEditpassword">确定</md-button>
      </md-dialog-actions>
    </md-dialog>

    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />
    <md-dialog-confirm
      :md-active.sync="confirmdialog"
      md-title="删除用户"
      md-content="确定要删除该用户吗?"
      md-confirm-text="确定"
      md-cancel-text="取消"
      @md-confirm="confirmDeleteUser"
    />
    <md-table v-model="users_items" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="用户名">{{ item.username }}</md-table-cell>
        <md-table-cell md-label="角色">
          <p v-if="item.role==0 ? true : false">系统管理员</p>
          <p v-if="item.role==1 ? true : false">库存管理员</p>
          <p v-if="item.role==2 ? true : false">进货管理员</p>
          <p v-if="item.role==3 ? true : false">销售管理员</p>
          <p v-if="item.role==4 ? true : false">入库员</p>
          <p v-if="item.role==5 ? true : false">销售员</p>
        </md-table-cell>
        <md-table-cell md-label="操作">
          <md-button v-bind:userid="item.id" v-on:click="deleteuser($event)">删除</md-button>
          <md-button
            class="md-primary"
            v-bind:itemid="item.id"
            v-bind:itemusername="item.username"
            v-bind:itemrole="item.role"
            v-on:click="modifyitem($event)"
          >编辑</md-button>
          <md-button
            class="md-success"
            v-bind:itemid="item.id"
            v-on:click="editpassword($event)"
          >修改密码</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "user-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      dialogcontent: "",
      popupdialog: false,
      deleteuserid: 0,
      confirmdialog: false,
      selected: [],
      currentusername: "",
      users_items: [],
      modifydialog: { show: false, itemdata: {} },
      passworddialog: {
        id: null,
        show: false,
        newpassword: null
      }
    };
  },
  mounted() {
    /*
    Vue.http.get("/checklogin").then(
      function(res) {
        if (res.status != 200) {
          window.location.href = "/index.html";
        }
      },
      function() {
        //document.write("Back-End");
      }
    ),*/
    this.getData();
  },
  methods: {
    getData() {
      Vue.http.get("/get_all_users").then(response => {
        window.console.log(response.body);
        this.users_items = response.body;
      });
    },
    deleteuser: function(e) {
      var userid = e.currentTarget.getAttribute("userid");

      if (userid == 1) {
        this.dialogcontent = "无法删除ID为1的用户！";
        this.popupdialog = true;
        return;
      } else {
        this.deleteuserid = userid;
        this.confirmdialog = true;
      }
    },
    confirmDeleteUser() {
      window.console.log("aaa");
      Vue.http
        .get("/deleteuser", { params: { id: this.deleteuserid } })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "ok") {
            this.dialogcontent = "删除成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.dialogcontent = "删除失败";
            this.popupdialog = true;
          }
        });
    },
    modifyitem: function(e) {
      this.modifydialog.itemdata.id = e.currentTarget.getAttribute("itemid");
      if (this.modifydialog.itemdata.id == 1) {
        this.dialogcontent = "无法编辑ID为1的用户！";
        this.popupdialog = true;
        return;
      }
      this.modifydialog.itemdata.username = e.currentTarget.getAttribute(
        "itemusername"
      );
      this.modifydialog.itemdata.role = e.currentTarget.getAttribute(
        "itemrole"
      );
      this.modifydialog.show = true;
    },
    editpassword: function(e) {
      this.passworddialog.id = e.currentTarget.getAttribute("itemid");
      this.passworddialog.show = true;
    },
    confirmEditpassword() {
      let sha256 = require("js-sha256").sha256;
      Vue.http
        .get("/editpassword", {
          params: {
            id: this.passworddialog.id,
            password: sha256(this.passworddialog.newpassword.toString() + "jfkH00H8Y3djiojernzwqiy31576Y8hahfhds")
          }
        })
        .then(response => {
          if (response.body == "ok") {
            this.passworddialog.show = false;
            this.dialogcontent = "修改成功";
            this.popupdialog = true;
          } else {
            this.passworddialog.show = false;
            this.dialogcontent = "修改失败";
            this.popupdialog = true;
          }
        });
      this.editpassword.show = false;
    },
    confirmModifyItem() {
      Vue.http
        .get("/modifyuser", {
          params: {
            id: this.modifydialog.itemdata.id,
            username: this.modifydialog.itemdata.username,
            role: this.modifydialog.itemdata.role
          }
        })
        .then(response => {
          if (response.body == "ok") {
            this.modifydialog.show = false;
            this.dialogcontent = "修改成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.modifydialog.show = false;
            this.dialogcontent = "修改失败";
            this.popupdialog = true;
          }
        });
      this.modifydialog.show = false;
    }
  }
};
</script>
