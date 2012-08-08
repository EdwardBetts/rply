from rply import ParserGenerator, Token

from .utils import FakeLexer, BoxInt


class TestBasic(object):
    def test_simple(self):
        pg = ParserGenerator(["VALUE"])

        @pg.production("main : VALUE")
        def main(p):
            return p[0]

        parser = pg.build()

        assert parser.parse(FakeLexer([Token("VALUE", "abc")])) == Token("VALUE", "abc")

    def test_arithmatic(self):
        pg = ParserGenerator(["NUMBER", "PLUS"])

        @pg.production("main : expr")
        def main(p):
            return p[0]

        @pg.production("expr : expr PLUS expr")
        def expr_op(p):
            return BoxInt(p[0].getint() + p[2].getint())

        @pg.production("expr : NUMBER")
        def expr_num(p):
            return BoxInt(int(p[0].getstr()))

        parser = pg.build()
        assert parser.parse(FakeLexer([
            Token("NUMBER", "1"),
            Token("PLUS", "+"),
            Token("NUMER", "4")
        ])) == BoxInt(5)
