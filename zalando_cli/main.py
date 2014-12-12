import click
import requests

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.group(invoke_without_command=True, cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    if not ctx.invoked_subcommand:
        r = requests.get('https://api.zalando.com/articles?pageSize=10')
        for article in r.json()['content']:
            click.secho(article['name'], bold=True, fg='blue')
            for unit in article['units']:
                click.secho('  ' + unit['price']['formatted'], bold=True, fg='green')
                click.secho('  SKU: {} Size: {}'.format(unit['id'], unit['size']))


def main():
    cli()
