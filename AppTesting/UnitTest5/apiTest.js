pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has correct character name", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.name).to.eql("Luke Skywalker");
});

pm.test("Character has films listed", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.films.length).to.be.above(0);
});

pm.test("Height is a number", function () {
    var jsonData = pm.response.json();
    pm.expect(parseInt(jsonData.height)).to.be.a("number");
});