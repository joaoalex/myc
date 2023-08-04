const express = require("express");
const path = require("path");
const sqlite3 = require("sqlite3").verbose();

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: false }));

const db_name = path.join(__dirname, "data", "database.sqlite");
const db = new sqlite3.Database(db_name, err => {
  if (err) {
    return console.error(err.message);
  }
  console.log("Ligação á BD ok");
});


// server
app.listen(3000, () => {
    console.log("Server listening (http://localhost:3000/) !");
});

// GET /
app.get("/", (req, res) => {
  // res.send("welcome");
  res.render("index");
});

// GET /about
app.get("/about", (req, res) => {
  res.render("about");
});

// GET /about
app.get("/gantt", (req, res) => {
  res.render("gantt");
});

app.get("/teams", (req, res) => {
  const sql = "SELECT * FROM teams ORDER BY name";
  db.all(sql, [], (err, rows) => {
    if (err) {
      return console.error(err.message);
    }
    res.render("teams", { model: rows });
  });
});

// GET /create
app.get("/create", (req, res) => {
  res.render("create", { model: {} });
});

// POST /create
app.post("/create", (req, res) => {
  var sql = "INSERT INTO teams (name, description, segment, metodologia, ativo,  createdAt, updatedAt) VALUES (?, ?, ?,?, ?,'', '')";
  const team = [req.body.name, req.body.description, req.body.segment, req.body.metodologia, req.body.ativo];
  console.log(team);
   
db.run(sql, team, err => {
    if (err) {
      return console.error(err.message);
    }
    db.get("SELECT id from teams where name = '" + team[0] + "'", function (err, row) {
      //console.log('Last inserted id is: ' + row['id']);
      console.log('Last inserted id is: ' , row);
      const roles=['Scrum Master', 'Product Owner', 'Agile Coach'];
      for (let i=0;i<roles.length;i++)
      {
      var role = [row['id'],roles[i]]
      sql="INSERT INTO roles (team, role,  createdAt, updatedAt) VALUES (?, ?,'','')";
      db.run(sql, role, err => {
          if (err) {
            return console.error(err.message);
          }
        });
      }
    res.redirect("/teams");
  });
   
});
});

// GET /edit
app.get("/edit/:id", (req, res) => {
  const id = req.params.id;
  const sql = "SELECT * FROM teams WHERE id = ?";
  db.get(sql, id, (err, row) => {
    if (err) {
      return console.error(err.message);
    }
    res.render("edit", { model: row });
  });
});

// POST /edit
app.post("/edit/:id", (req, res) => {
  const id = req.params.id;
  const team = [req.body.name, req.body.description, req.body.segment, req.body.metodologia, req.body.ativo, id];
  const sql = "UPDATE teams SET name = ?, description = ?, segment= ?, metodologia = ?, ativo = ? WHERE (id = ?)";
  db.run(sql, team, err => {
    if (err) {
      return console.error(err.message);
    }
    res.redirect("/teams");
  });
});

// GET /delete
app.get("/delete/:id", (req, res) => {
  const id = req.params.id;
  const sql = "SELECT * FROM teams WHERE id = ?";
  db.get(sql, id, (err, row) => {
    if (err) {
      return console.error(err.message);
    }
    res.render("delete", { model: row });
  });
});

// POST /delete
app.post("/delete/:id", (req, res) => {
  const id = req.params.id;
  const sql = "DELETE FROM teams WHERE id = ?";
  db.run(sql, id, err => {
    if (err) {
      return console.error(err.message);
    }
    res.redirect("/teams");
  });
});

