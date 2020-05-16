<?php
/**
 * Template footer, included in the main and detail files
 */

// must be run from within DokuWiki
if (!defined('DOKU_INC')) die();
?>

<!-- ********** FOOTER ********** -->
<div id="dokuwiki__footer"><div class="pad">
    <!--<?php tpl_license(''); // license text ?>-->
    The content of this wiki is licensed by <a href="http://spielend-programmieren.at/en:kontakt">Horst JENS</a> under <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative-Commons Attribution-Share-alike 4.0 international license (cc-by-sa 4.0)</a>
    <span class="buttons">
        <?php
            tpl_license('button', true, false, false); // license button, no wrapper
            $target = ($conf['target']['extern']) ? 'target="'.$conf['target']['extern'].'"' : '';
        ?>
        <a href="http://spielend-programmieren.at/en:kontakt#donation" title="Donate" <?php echo $target?>><img
            src="<?php echo tpl_basedir(); ?>images/button-donate.gif" width="80" height="15" alt="Donate" /></a>
        <a href="https://dokuwiki.org/" title="Driven by DokuWiki" <?php echo $target?>><img
            src="<?php echo tpl_basedir(); ?>images/button-dw.png" width="80" height="15" alt="Driven by DokuWiki" /></a>
    </span>
</div></div><!-- /footer -->

<?php
tpl_includeFile('footer.html');
