module.exports = (sequelize, DataTypes) => {
  const Teams = sequelize.define("teams", {
    name: {
      type: DataTypes.STRING
    },
    description: {
      type: DataTypes.STRING
    },
    metodologia: {
      type: DataTypes.STRING
    },
    ativo: {
      type: DataTypes.BOOLEAN
    },
    questjson: {
      type: DataTypes.TEXT('long')
    },
    segment: {
      type: DataTypes.STRING
    },
  });

  return Teams;
 
};
